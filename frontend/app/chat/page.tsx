// filepath: /home/prajwalak/Desktop/di/next_frontend/src/app/rag-chat/page.tsx
"use client";

import { useEffect, useState, useRef, useCallback } from "react";
import { Loader2 } from "lucide-react";
import ReactMarkdown, { Components } from "react-markdown";
import remarkGfm from "remark-gfm";
import rehypeRaw from "rehype-raw";
import ChatTextBox from "@/app/chat/ChatTextBox";
import { ScrollArea } from "@/components/ui/scroll-area";

interface ChatMessage {
  content: string;
  role: "user" | "assistant";
  confidence?: number;
  reasoning?: string;
}

const markdownComponents: Components = {
  h1: ({ children }) => (
    <h1 className="text-3xl font-bold mt-8 mb-4 text-black">{children}</h1>
  ),
  h2: ({ children }) => (
    <h2 className="text-2xl font-semibold mt-6 mb-3 text-black">{children}</h2>
  ),
  h3: ({ children }) => (
    <h3 className="text-xl font-medium mt-4 mb-2 text-black">{children}</h3>
  ),
  p: ({ children }) => (
    <p className="text-xl leading-relaxed mb-4 text-black">{children}</p>
  ),
  ul: ({ children }) => (
    <ul className="list-disc text-xl pl-6 mb-4 space-y-2 text-black">{children}</ul>
  ),
  ol: ({ children }) => (
    <ol className="list-decimal pl-6 mb-4 space-y-2 text-black">{children}</ol>
  ),
  li: ({ children }) => <li className="pl-2">{children}</li>,
  a: ({ children, href }) => (
    <a
      href={href}
      className="text-blue-400 hover:text-blue-300 underline"
      target="_blank"
      rel="noopener noreferrer"
    >
      {children}
    </a>
  ),
};

export default function RagChatPage() {
  const [input, setInput] = useState("");
  const [sessionId, setSessionId] = useState("first_session");
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [isLoading, setIsLoading] = useState(false);

  const scrollToBottom = useCallback(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, []);

  useEffect(() => {
    scrollToBottom();
  }, [messages, isLoading, scrollToBottom]);

  const handleInputChange = (value: string) => setInput(value);

  const fetchResponse = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim() || isLoading) return;

    setIsLoading(true);
    const newMessage: ChatMessage = { content: input, role: "user" };
    setMessages(prev => [...prev, newMessage]);
    setInput("");

    try {
      const response = await fetch("http://localhost:8000/rag-chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ query: input, session_id: sessionId }),
      });

      if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
      
      const data = await response.json();
      if (data.response) {
        setSessionId(data.response.session_id);
        setMessages(prev => [
          ...prev,
          {
            content: data.response.answer.replace(/\n/g, "\n\n"),
            role: "assistant",
            confidence: data.response.confidence,
            reasoning: data.response.reasoning,
          }
        ]);
      }
    } catch (error) {
      console.error("Fetch error:", error);
      setMessages(prev => [
        ...prev,
        {
          content: "Sorry, I'm having trouble responding. Please try again later.",
          role: "assistant"
        }
      ]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="flex h-screen w-full bg-white">
      <div className="flex-1 pb-12 flex flex-col max-w-4xl mx-auto">
        <ScrollArea className="flex-1 px-4 pt-8 pb-24">
          <div className="space-y-8">
            {messages.map((msg, index) => (
              <div
                key={index}
                className={`flex ${msg.role === "user" ? "justify-end" : "justify-start"}`}
              >
                <div
                  className={`max-w-[85%] rounded-3xl ${
                    msg.role === "user"
                      ? "bg-gray-100 text-black"
                      : "bg-white text-black"
                  }`}
                >
                  {msg.role === "assistant" && (
                    <div className="px-6 border-b border-zinc-700/50 flex items-center space-x-3">
                      <div className="w-7 h-7 rounded-full bg-white flex items-center justify-center">
                        <span className="text-blue-400 text-lg">🤖</span>
                      </div>
                      <span className="text-sm font-medium text-blue-400">
                        AI Assistant
                      </span>
                    </div>
                  )}
                  <div className="p-5">
                    <ReactMarkdown
                      remarkPlugins={[remarkGfm]}
                      rehypePlugins={[rehypeRaw]}
                      components={markdownComponents}
                      className="prose prose-invert max-w-none"
                    >
                      {msg.content}
                    </ReactMarkdown>
                  </div>
                </div>
              </div>
            ))}
            {isLoading && (
              <div className="flex justify-start">
                <div className="w-full max-w-[85%] rounded-3xl shadow-lg bg-zinc-800/50">
                  <div className="px-6 py-3 border-b border-zinc-700/50 flex items-center space-x-3">
                    <div className="w-7 h-7 rounded-full bg-white flex items-center justify-center">
                      <Loader2 className="h-4 w-4 animate-spin text-blue-400" />
                    </div>
                    <span className="text-sm font-medium text-blue-400">
                      AI Assistant
                    </span>
                  </div>
                  <div className="p-5 space-y-4">
                    <div className="h-4 w-3/4 bg-zinc-700/50 rounded-full animate-pulse" />
                    <div className="h-4 w-2/3 bg-zinc-700/50 rounded-full animate-pulse" />
                    <div className="h-4 w-1/2 bg-zinc-700/50 rounded-full animate-pulse" />
                  </div>
                </div>
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>
        </ScrollArea>

        <div className="absolute bottom-0 left-0 right-0">
          <div className="max-w-4xl mx-auto px-4 py-6 z-10">
            <form onSubmit={fetchResponse}>
              <ChatTextBox
                value={input}
                onChange={handleInputChange}
                placeholder="Type your message... (Shift + Enter for new line)"
                className="w-full bg-gray-200 text-xl border border-gray-200 active:border-gray-200"
                disabled={isLoading}
              />
            </form>
          </div>
        </div>
      </div>
    </div>
  );
}