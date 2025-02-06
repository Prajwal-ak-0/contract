"use client";

import React from 'react';
import { Textarea } from '@/components/ui/textarea';
import { SendHorizontal } from 'lucide-react';

interface ChatTextBoxProps {
  value: string;
  onChange: (value: string) => void;
  onSubmit: (e: React.FormEvent) => void;
  placeholder?: string;
  className?: string;
  disabled?: boolean;
}

const ChatTextBox: React.FC<ChatTextBoxProps> = ({
  value,
  onChange,
  onSubmit,
  placeholder,
  className,
  disabled
}) => {
  const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      if (value.trim()) {
        onSubmit(e as unknown as React.FormEvent);
      }
    }
  };

  return (
    <div className="fixed bottom-0 left-0 right-0 p-4">
      <form onSubmit={onSubmit} className="max-w-4xl mx-auto relative">
        <Textarea
          value={value}
          onChange={(e) => onChange(e.target.value)}
          placeholder={placeholder}
          className={`min-h-[90px] max-h-[400px] flex flex-1 w-full pt-4 pb-10 pl-5 pr-12 resize-none focus:outline-none text-3xl bg-white text-black rounded-3xl border border-gray-200 active:border-gray-200 placeholder:text-xl ${className}`}
          disabled={disabled}
          rows={2}
          onKeyDown={handleKeyDown}
        />
        <button 
          type="submit"
          className="absolute right-4 bottom-4 p-2 text-neutral-400 hover:text-neutral-100 bg-gray-900 hover:bg-neutral-700 rounded-xl transition-colors duration-200 cursor-pointer"
          disabled={disabled || !value.trim()}
        >
          <SendHorizontal className="h-5 w-5" />
        </button>
      </form>
    </div>
  );
};

export default ChatTextBox;