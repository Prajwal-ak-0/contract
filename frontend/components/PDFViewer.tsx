import React, { useState, useEffect, useRef, useCallback } from 'react';
import { GlobalWorkerOptions, getDocument, PDFDocumentProxy } from 'pdfjs-dist';
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { toast } from "sonner";

// Set worker path
GlobalWorkerOptions.workerSrc = '/pdf.worker.min.mjs';

interface PdfViewerProps {
  file: File | null;
  currentPage: number;
  setCurrentPage: (page: number) => void;
  onClose: () => void;
  textToHighlight?: string;
}

export default function PdfViewer({ file, currentPage, setCurrentPage, onClose, textToHighlight }: PdfViewerProps) {
  const [pdfDoc, setPdfDoc] = useState<PDFDocumentProxy | null>(null);
  const [totalPages, setTotalPages] = useState(0);
  const [scale, setScale] = useState(1);
  const [isRendering, setIsRendering] = useState(false);
  const [searchPage, setSearchPage] = useState<string>('');
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const containerRef = useRef<HTMLDivElement>(null);
  const pdfPageRef = useRef<any>(null);
  const currentRenderTask = useRef<any>(null);

  // Function to highlight text on the page
  const highlightText = useCallback(async (page: any, viewport: any) => {
    if (!textToHighlight?.trim() || !containerRef.current) {
      console.log('No text to highlight or container not ready');
      return;
    }

    try {
      console.log('Highlighting text:', textToHighlight);

      // Clean up existing highlights
      containerRef.current.querySelectorAll('.text-highlight').forEach(el => el.remove());

      // Get text content with specific parameters
      const textContent = await page.getTextContent({
        normalizeWhitespace: false,
        disableCombineTextItems: true
      });

      // Create highlight layer if it doesn't exist
      let highlightLayer = containerRef.current.querySelector('.highlight-layer') as HTMLDivElement | null;
      if (!highlightLayer) {
        highlightLayer = document.createElement('div');
        highlightLayer.className = 'highlight-layer';
        highlightLayer.style.position = 'absolute';
        highlightLayer.style.left = '0';
        highlightLayer.style.top = '0';
        highlightLayer.style.width = '100%';
        highlightLayer.style.height = '100%';
        highlightLayer.style.pointerEvents = 'none';
        highlightLayer.style.zIndex = '1';
        containerRef.current.appendChild(highlightLayer);
      }

      // Function to normalize text for comparison
      const normalizeText = (text: string) => {
        // Remove any quotes and normalize whitespace
        return text.replace(/['"]/g, '').trim().replace(/\s+/g, ' ');
      };

      // Function to find exact match
      const findExactMatch = (str: string, searchText: string) => {
        const normalizedStr = normalizeText(str);
        const normalizedSearch = normalizeText(searchText);
        const index = normalizedStr.indexOf(normalizedSearch);
        
        if (index === -1) return null;

        // Check if it's a standalone match
        const beforeChar = index > 0 ? normalizedStr[index - 1] : ' ';
        const afterChar = index + normalizedSearch.length < normalizedStr.length ? 
          normalizedStr[index + normalizedSearch.length] : ' ';

        // Only consider it a match if it's a complete match
        if ((/[\s.,()"]/.test(beforeChar) || index === 0) && 
            (/[\s.,()"]/.test(afterChar) || index + normalizedSearch.length === normalizedStr.length)) {
          return {
            start: index,
            end: index + normalizedSearch.length,
            text: normalizedStr.substring(index, index + normalizedSearch.length)
          };
        }

        return null;
      };

      // Find matching text items
      for (const item of textContent.items) {
        if (!item.str) continue;
        
        console.log('Checking item:', JSON.stringify(item.str));
        
        const match = findExactMatch(item.str, textToHighlight);
        if (!match) continue;

        console.log('Found exact match:', match);

        // Create highlight element
        const highlight = document.createElement('div');
        highlight.className = 'text-highlight';
        highlight.style.position = 'absolute';
        highlight.style.backgroundColor = 'yellow';
        highlight.style.opacity = '0.3';
        highlight.style.mixBlendMode = 'multiply';
        highlight.style.pointerEvents = 'none';

        // Calculate text position in viewport coordinates
        const tx = item.transform[4];
        const ty = item.transform[5];
        
        // Calculate the offset and width based on character positions
        const beforeWidth = (match.start / item.str.length) * item.width;
        const matchWidth = ((match.end - match.start) / item.str.length) * item.width;
        
        // Convert to viewport coordinates
        const [x, y] = viewport.convertToViewportPoint(tx + beforeWidth, ty);
        
        console.log('PDF coordinates:', { tx: tx + beforeWidth, ty });
        console.log('Viewport coordinates:', { x, y });

        // Calculate dimensions
        const width = matchWidth * viewport.scale;
        const height = item.height * viewport.scale;

        // Position highlight with 50px offset
        highlight.style.left = `${(x * scale) + 50}px`;
        highlight.style.top = `${(y - height) * scale}px`;
        highlight.style.width = `${width * scale}px`;
        highlight.style.height = `${height * scale}px`;

        console.log('Created highlight:', {
          text: match.text,
          position: { x, y },
          dimensions: { width, height }
        });

        highlightLayer.appendChild(highlight);
        // Only highlight the first exact match
        break;
      }
    } catch (error) {
      console.error('Error highlighting text:', error);
    }
  }, [textToHighlight, scale]);

  // Render PDF page
  const renderPage = useCallback(async () => {
    if (!pdfDoc || !canvasRef.current) return;

    try {
      const page = await pdfDoc.getPage(currentPage);
      const viewport = page.getViewport({ scale });
      const canvas = canvasRef.current;
      const context = canvas.getContext('2d');

      if (!context) return;

      // Clear previous content
      context.clearRect(0, 0, canvas.width, canvas.height);

      // Set canvas dimensions
      canvas.height = viewport.height;
      canvas.width = viewport.width;

      const renderContext = {
        canvasContext: context,
        viewport: viewport,
        enableWebGL: false,
        renderInteractiveForms: false
      };

      // Cancel any ongoing render operation
      if (currentRenderTask.current) {
        currentRenderTask.current.cancel();
      }

      // Start new render task
      currentRenderTask.current = page.render(renderContext);
      
      try {
        await currentRenderTask.current.promise;
        
        // After render completes, highlight text if needed
        if (textToHighlight) {
          await highlightText(page, viewport);
        }
      } catch (error) {
        if (error?.name === 'RenderingCancelled') {
          console.log('Rendering was cancelled');
        } else {
          console.error('Error rendering page:', error);
        }
      }
    } catch (error) {
      console.error('Error rendering page:', error);
    }
  }, [pdfDoc, currentPage, scale, textToHighlight, highlightText]);

  useEffect(() => {
    if (file) {
      const reader = new FileReader();
      reader.onload = async (e) => {
        const data = e.target?.result as ArrayBuffer;
        try {
          const loadingTask = getDocument({ data });
          const pdf = await loadingTask.promise;
          setPdfDoc(pdf);
          setTotalPages(pdf.numPages);
          setCurrentPage(1);
        } catch (err) {
          console.error('Error loading PDF:', err);
          toast.error('Error loading PDF. Please try again.');
        }
      };
      reader.readAsArrayBuffer(file);
    }
  }, [file, setCurrentPage]);

  useEffect(() => {
    if (pdfDoc) {
      renderPage();
    }
  }, [pdfDoc, currentPage, scale, renderPage]);

  useEffect(() => {
    if (pdfPageRef.current && textToHighlight) {
      highlightText(pdfPageRef.current, pdfPageRef.current.getViewport({ scale: 1 }));
    }
  }, [highlightText, textToHighlight]);

  const handleZoomIn = () => setScale(prevScale => prevScale + 0.25);
  
  const handleZoomOut = () => {
    setScale(prevScale => Math.max(0.5, prevScale - 0.25));
  };

  const handlePageChange = (newPage: number) => {
    if (newPage >= 1 && newPage <= totalPages) {
      setCurrentPage(newPage);
    }
  };

  const handleSearchPage = () => {
    const pageNum = parseInt(searchPage);
    if (!isNaN(pageNum)) {
      handlePageChange(pageNum);
    }
  };

  return (
    <div className="bg-white shadow overflow-hidden sm:rounded-lg p-4">
      <h2 className="text-2xl font-bold text-gray-900 mb-4">PDF Viewer</h2>

      <div className="flex justify-between items-center mb-4">
        <div className="flex items-center">
          <Input
            type="number"
            min="1"
            max={totalPages}
            value={searchPage}
            onChange={(e) => setSearchPage(e.target.value)}
            className="border p-2 mr-2 w-24"
            placeholder={`Page (1-${totalPages})`}
            style={{ appearance: 'textfield' }}
          />
          <Button onClick={handleSearchPage} disabled={isRendering || searchPage === ''}>
            Go
          </Button>
        </div>
        <div>
          <Button onClick={() => handlePageChange(currentPage - 1)} disabled={currentPage <= 1} className="mr-2">
            Previous
          </Button>
          <Button onClick={() => handlePageChange(currentPage + 1)} disabled={currentPage >= totalPages}>
            Next
          </Button>
        </div>
        <span className="text-gray-700">
          Page {currentPage} of {totalPages}
        </span>
        <div>
          <Button onClick={handleZoomOut} disabled={scale <= 0.5} className="mr-2">
            Zoom Out
          </Button>
          <Button onClick={handleZoomIn}>
            Zoom In
          </Button>
        </div>
      </div>

      <div
        ref={containerRef}
        className="relative border border-gray-300 rounded-lg overflow-auto" style={{ height: '600px' }}
      >
        <canvas ref={canvasRef} className="mx-auto"></canvas>
      </div>
      <div className="flex justify-end mt-4">
        <Button onClick={onClose}>Close</Button>
      </div>
    </div>
  );
}