"use client"

import React from "react";
import { Label } from "@/components/ui/label";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { useRouter } from "next/navigation";

interface FileUploadProps {
  handleFileChange: (e: React.ChangeEvent<HTMLInputElement>) => void;
  pdfType: string;
  handlePdfTypeChange: (value: string) => void;
  handleFileUpload: () => void;
  file: File | null;
  isUploading: boolean;
  isFileUploaded: boolean;
}

const FileUpload: React.FC<FileUploadProps> = ({
  handleFileChange,
  pdfType,
  handlePdfTypeChange,
  handleFileUpload,
  file,
  isUploading,
  isFileUploaded,
}) => {
  const router = useRouter();
  return (
    <div className="mt-8">
      <Label htmlFor="file-upload">Upload PDF</Label>
      <div className="mt-1 flex items-center gap-x-4">
        <Input
          id="file-upload"
          type="file"
          onChange={handleFileChange}
          className="text-black"
          accept=".pdf"
        />
        <Select value={pdfType} onValueChange={handlePdfTypeChange}>
          <SelectTrigger className="w-[180px]">
            <SelectValue placeholder="Select PDF type" />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value="SOW">SOW</SelectItem>
            <SelectItem value="MSA">MSA</SelectItem>
          </SelectContent>
        </Select>
      </div>
      <div className="flex mt-4 gap-x-4">
      <Button
        onClick={handleFileUpload}
        disabled={!file || isUploading}
      >
        {isUploading ? "Uploading..." : "Upload PDF"}
      </Button>
      <Button 
         onClick={() => router.push("/chat")}
         disabled={!file || isUploading || !isFileUploaded}
      >
          Chat
      </Button>
      </div>
    </div>
  );
};

export default FileUpload;