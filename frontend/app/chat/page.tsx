// filepath: /home/prajwalak/Desktop/di/next_frontend/src/app/rag-chat/page.tsx
"use client";

import { useEffect, useState ,useRef } from "react";
import { Loader2 } from "lucide-react";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import rehypeRaw from "rehype-raw";
import { PrismLight as SyntaxHighlighter } from "react-syntax-highlighter";
import { vscDarkPlus } from "react-syntax-highlighter/dist/esm/styles/prism";
import ChatTextBox from "@/app/chat/ChatTextBox";
import { ScrollArea } from "@/components/ui/scroll-area";

// eslint-disable-next-line @typescript-eslint/no-explicit-any
const CodeComponent = ({ inline, className, children, ...props }: any) => {
  const match = /language-(\w+)/.exec(className || '');
  return !inline && match ? (
    <SyntaxHighlighter
      style={vscDarkPlus}
      language={match[1]}
      PreTag="div"
      {...props}
    >
      {String(children).replace(/\n$/, '')}
    </SyntaxHighlighter>
  ) : (
    <code className={className} {...props}>
      {children}
    </code>
  );
};

export default function RagChatPage() {

  const [input, setInput] = useState<string>("");
  const [sessionId, setSessionId] = useState<string >("first_session");
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const [messages, setMessages] = useState<any[]>([]);
  const [isLoading, setIsLoading] = useState<boolean>(false);

  const handleInputChange = (value: string) => {
    setInput(value);
  };

  const fetchResponse = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim()) return;

    setIsLoading(true);
    setMessages(prev => [...prev, { content: input, role: 'user' }]);
    setInput('');

    try {
      const response = await fetch("http://localhost:8000/rag-chat", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          query: input,
          session_id: sessionId // Initially null, then use received session_id
        }),
      });
      
      const data = await response.json();
      console.log("Response:", data);

      if (data.response) {
        // Update session ID from response
        setSessionId(data.response.session_id);
        
        // Add assistant message with answer from response
        setMessages(prev => [...prev, { 
          content: data.response.answer,
          role: 'assistant',
          confidence: data.response.confidence,
          reasoning: data.response.reasoning
        }]);
      }
    } catch (error) {
      console.error("Error fetching response:", error);
    } finally {
      setIsLoading(false);
    }
  };


  return (
    <div className="flex h-screen w-screen bg-gradient-to-b from-gray-900 via-gray-900 to-black">
      <div className="flex-1 flex flex-col">

        {/* Chat container */}
        <div className="flex-1 overflow-hidden flex flex-col">
          <div className="relative w-full max-w-4xl mx-auto h-full flex flex-col">
            <div className="flex-1 flex flex-col bg-transparent border-none overflow-hidden">
              <ScrollArea className="flex-1 px-2 mb-24 mt-10">
                <div className="space-y-8">
                  {Array.isArray(messages) && messages.length > 0 ? (
                    <>
                      {messages.map((msg, index) => (
                        <div
                          key={index}
                          className={`flex ${
                            msg.role === "user" ? "justify-end ml-64" : "justify-start"
                          } ${index > 0 ? "mt-6" : ""}`}
                        >
                          <div
                            className={`max-w-[85%] rounded-3xl shadow-lg ${
                              msg.role === "user"
                                ? "bg-blue-600/20 text-blue-50 ml-40 font-sans font-light"
                                : "bg-zinc-800/30 text-zinc-100 mr-12"
                            }`}
                          >
                            {msg.role === "assistant" && (
                              <div className="px-6 py-2 border-b border-zinc-700/50 flex items-center space-x-2">
                                <div className="w-6 h-6 rounded-full bg-blue-600/20 flex items-center justify-center">
                                  <span className="text-blue-400 text-sm">🤖</span>
                                </div>
                                <span className="text-sm font-medium text-blue-400">AI Assistant</span>
                              </div>
                            )}
                            <div className="p-4">
                              <ReactMarkdown
                                remarkPlugins={[remarkGfm]}
                                rehypePlugins={[rehypeRaw]}
                                className="prose prose-invert max-w-none"
                                components={{
                                  code: CodeComponent,
                                }}
                              >
                                {msg.content}
                              </ReactMarkdown>
                            </div>
                          </div>
                        </div>
                      ))}
                      {isLoading && (
                        <div className="flex justify-start mt-6 w-full">
                          <div className="w-full rounded-3xl shadow-lg bg-zinc-800/50 text-zinc-100 mr-32">
                            <div className="px-6 py-2 border-b border-zinc-700/50 flex items-center space-x-2">
                              <div className="w-6 h-6 rounded-full bg-blue-600/20 flex items-center justify-center">
                                <Loader2 className="h-4 w-4 animate-spin text-blue-400" />
                              </div>
                              <span className="text-sm font-medium text-blue-400">AI Assistant</span>
                            </div>
                            <div className="p-8">
                              <div className="space-y-4">
                                <div className="h-4 w-3/4 bg-zinc-700/50 rounded-full animate-pulse" />
                                <div className="h-4 w-2/3 bg-zinc-700/50 rounded-full animate-pulse" />
                                <div className="h-4 w-1/2 bg-zinc-700/50 rounded-full animate-pulse" />
                              </div>
                            </div>
                          </div>
                        </div>
                      )}
                    </>
                  ) : (
                    <div className="flex flex-col items-center justify-center h-full py-12 text-center">
                      <div className="text-zinc-400 space-y-2">
                        <p className="text-lg font-medium">No messages yet</p>
                        <p className="text-sm">Start a conversation by typing a message below</p>
                      </div>
                    </div>
                  )}
                  <div ref={messagesEndRef} />
                </div>
              </ScrollArea>

              <div className="p-4">
                <form onSubmit={fetchResponse} className="flex space-x-3">
                  <ChatTextBox
                    value={input}
                    onChange={handleInputChange}
                    placeholder="Type your message... (Press Enter to send)"
                    className="flex-1"
                    disabled={isLoading}
                  />
                </form>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}