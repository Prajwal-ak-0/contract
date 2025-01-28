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

  return (
    <div className="fixed bottom-0 left-0 right-0  p-4">
      <div className="max-w-4xl mx-auto relative">
        <Textarea
          value={value}
          onChange={(e) => onChange(e.target.value)}
          placeholder={placeholder}
          className={`min-h-[90px] max-h-[400px] flex flex-1 w-full pt-4 pb-10 pl-5 pr-12 resize-none focus:outline-none text-3xl bg-white text-black rounded-3xl border border-gray-200 active:border-gray-200 placeholder:text-xl ${className}`}
          disabled={disabled}
          rows={2}
        />
        <button 
          type="submit"
          className="absolute right-4 bottom-4 p-2 text-neutral-400 hover:text-neutral-100 bg-gray-900 hover:bg-neutral-700 rounded-xl transition-colors duration-200 cursor-pointer"
          disabled={disabled || !value.trim()}
        >
          <SendHorizontal className="h-5 w-5" />
        </button>
      </div>
    </div>
  );
};

export default ChatTextBox;