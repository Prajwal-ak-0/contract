"use client";

import React from 'react';
import { Textarea } from '@/components/ui/textarea';
import { SendHorizontal } from 'lucide-react';

interface ChatTextBoxProps {
  value: string;
  onChange: (value: string) => void;
  placeholder?: string;
  className?: string;
  disabled?: boolean;
}

const ChatTextBox: React.FC<ChatTextBoxProps> = ({
  value,
  onChange,
  placeholder,
  className,
  disabled
}) => {
  // const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
  //   if (e.key === 'Enter' && !e.shiftKey) {
  //     e.preventDefault();
  //     const form = e.currentTarget.form;
  //     if (form) {
  //       form.dispatchEvent(new Event('submit', { cancelable: true }));
  //     }
  //   }
  // };

  return (
    <div className="fixed bottom-0 left-0 right-0  p-4">
      <div className="max-w-4xl mx-auto relative">
        <Textarea
          value={value}
          onChange={(e) => onChange(e.target.value)}
          placeholder={placeholder}
          className={`min-h-[90px] max-h-[400px] flex flex-1 w-full pt-4 pb-10 pl-5 pr-12 resize-none focus:outline-none focus:border-neutral-500 cursor-text text-lg bg-neutral-700/70 border-2 border-neutral-800 text-neutral-100 placeholder:text-neutral-600 rounded-3xl ${className}`}
          disabled={disabled}
          // onKeyDown={handleKeyDown}
          rows={2}
        />
        <button 
          type="submit"
          className="absolute right-4 bottom-4 p-2 text-neutral-400 hover:text-neutral-100 bg-neutral-800 hover:bg-neutral-700 rounded-xl transition-colors duration-200"
          disabled={disabled || !value.trim()}
        >
          <SendHorizontal className="h-5 w-5" />
        </button>
      </div>
    </div>
  );
};

export default ChatTextBox;