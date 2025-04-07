"use client";

import React from "react";
import { Button } from "@/components/ui/button";
import Link from "next/link";
import { 
  ArrowRight, 
  FileText, 
  MessageSquare, 
  Zap,
  PieChart,
  Database,
  MousePointer,
  Edit,
  ExternalLink,
  HelpCircle,
  AlertCircle
} from "lucide-react";

export default function LandingPage() {
  return (
    <div className="min-h-screen bg-gradient-to-b from-white to-gray-50">
      {/* Hero Section with consistent styling */}
      <section className="w-full py-20 md:py-28 lg:py-36 relative overflow-hidden">
        <div className="container px-4 md:px-6 mx-auto">
          <div className="flex flex-col items-center text-center max-w-4xl mx-auto">
            <div className="mb-8">
              <h1 className="text-5xl md:text-6xl lg:text-7xl font-bold tracking-tighter text-black mb-8 leading-tight">
                Intelligent Contract Analysis
              </h1>
              <p className="text-xl md:text-2xl text-gray-700 max-w-3xl mx-auto mt-6">
                Extract key information, analyze terms, and get AI-powered insights from your contracts in seconds.
              </p>
            </div>

            {/* Clean Feature Grid */}
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4 md:gap-6 my-10 w-full max-w-4xl">
              {[
                { text: "SOW Analysis", icon: <FileText className="mb-2 h-6 w-6" /> },
                { text: "Term Extraction", icon: <Database className="mb-2 h-6 w-6" /> },
                { text: "Data Visualization", icon: <PieChart className="mb-2 h-6 w-6" /> },
                { text: "Excel Export", icon: <ExternalLink className="mb-2 h-6 w-6" /> },
              ].map((item, i) => (
                <div
                  key={i}
                  className="flex flex-col items-center justify-center p-4 bg-white rounded-xl shadow-sm border border-gray-100 hover:shadow-md transition-all duration-200 text-black"
                >
                  {item.icon}
                  <span className="font-medium">{item.text}</span>
                </div>
              ))}
            </div>

            <div className="flex flex-col sm:flex-row gap-4 w-full max-w-md mx-auto">
              <Link href="/contract" className="w-full">
                <Button className="w-full h-14 px-8 text-base font-medium bg-black text-white hover:bg-gray-800 transition-all duration-200 shadow-lg">
                  Upload Contract <ArrowRight className="ml-2 h-5 w-5" />
                </Button>
              </Link>
              <div className="relative w-full group">
                <Button 
                  className="w-full h-14 px-8 text-base font-medium bg-gray-300 text-gray-700 cursor-not-allowed opacity-80 shadow-lg"
                  disabled
                >
                  AI Chat <AlertCircle className="ml-2 h-5 w-5" />
                </Button>
                <div className="absolute -top-10 left-0 right-0 bg-black text-white p-2 rounded text-sm text-center opacity-0 group-hover:opacity-100 transition-opacity">
                  Please upload a contract document first
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* How It Works - Simple 3-Step Process */}
      <section className="w-full py-20 bg-white border-t border-gray-100">
        <div className="container px-4 md:px-6 mx-auto">
          <div className="text-center mb-16">
            <h2 className="text-4xl font-bold text-black mb-4">
              How It Works
            </h2>
            <p className="text-xl text-gray-700 max-w-2xl mx-auto">
              Our simple 3-step process makes contract analysis effortless
            </p>
          </div>

          <div className="max-w-5xl mx-auto">
            <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
              {[
                {
                  step: "1",
                  title: "Upload Contract",
                  description: "Upload your PDF contract document to our secure platform",
                  icon: <Database className="h-8 w-8" />
                },
                {
                  step: "2",
                  title: "Automatic Analysis",
                  description: "Our AI extracts key terms, dates, amounts and other critical information",
                  icon: <Zap className="h-8 w-8" />
                },
                {
                  step: "3",
                  title: "Review and Export",
                  description: "Review the extracted data, chat with AI, and download your report",
                  icon: <FileText className="h-8 w-8" />
                }
              ].map((item, index) => (
                <div
                  key={index}
                  className="flex flex-col items-center text-center p-6 bg-gray-50 rounded-xl hover:shadow-md transition-all duration-200"
                >
                  <div className="flex items-center justify-center w-14 h-14 rounded-full bg-black text-white shadow-lg mb-4">
                    {item.icon}
                  </div>
                  <h3 className="text-xl font-bold text-black mb-2">{item.title}</h3>
                  <p className="text-gray-700">{item.description}</p>
                </div>
              ))}
            </div>
          </div>
        </div>
      </section>

      {/* User Guide Table */}
      <section className="w-full py-20 bg-gray-50 border-t border-gray-100">
        <div className="container px-4 md:px-6 mx-auto">
          <div className="text-center mb-16">
            <h2 className="text-4xl font-bold text-black mb-4">
              Features Guide
            </h2>
            <p className="text-xl text-gray-700 max-w-2xl mx-auto">
              Key capabilities to help you analyze contracts efficiently
            </p>
          </div>

          <div className="max-w-5xl mx-auto bg-white rounded-xl shadow-md overflow-hidden">
            <div className="overflow-x-auto">
              <table className="w-full">
                <thead className="bg-black text-white">
                  <tr>
                    <th className="py-4 px-6 text-left">Feature</th>
                    <th className="py-4 px-6 text-left">Description</th>
                    <th className="py-4 px-6 text-left">How to Use</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-gray-200 text-black">
                  <tr className="hover:bg-gray-50">
                    <td className="py-4 px-6 font-medium flex items-center">
                      <MousePointer className="h-5 w-5 inline mr-2" />
                      Field Navigation
                    </td>
                    <td className="py-4 px-6">
                      Click on any field row to navigate to the specific page in the PDF
                    </td>
                    <td className="py-4 px-6 text-gray-800">
                      Click any row in the data table to jump to the relevant page
                    </td>
                  </tr>
                  <tr className="hover:bg-gray-50">
                    <td className="py-4 px-6 font-medium flex items-center">
                      <HelpCircle className="h-5 w-5 inline mr-2" />
                      Field Information
                    </td>
                    <td className="py-4 px-6">
                      Hover over field names to see detailed reasoning
                    </td>
                    <td className="py-4 px-6 text-gray-800">
                      Move your cursor over any field name to view AI reasoning
                    </td>
                  </tr>
                  <tr className="hover:bg-gray-50">
                    <td className="py-4 px-6 font-medium flex items-center">
                      <Edit className="h-5 w-5 inline mr-2" />
                      Edit Data
                    </td>
                    <td className="py-4 px-6">
                      Edit extracted field values if corrections are needed
                    </td>
                    <td className="py-4 px-6 text-gray-800">
                      Click the edit button on any row to modify the value
                    </td>
                  </tr>
                  <tr className="hover:bg-gray-50">
                    <td className="py-4 px-6 font-medium flex items-center">
                      <ExternalLink className="h-5 w-5 inline mr-2" />
                      Export Data
                    </td>
                    <td className="py-4 px-6">
                      Download all extracted contract data as an Excel spreadsheet
                    </td>
                    <td className="py-4 px-6 text-gray-800">
                      Click the &quot;Download Excel Report&quot; button
                    </td>
                  </tr>
                  <tr className="hover:bg-gray-50">
                    <td className="py-4 px-6 font-medium flex items-center">
                      <MessageSquare className="h-5 w-5 inline mr-2" />
                      AI Chat
                    </td>
                    <td className="py-4 px-6">
                      Chat with an AI about your contract to get insights
                    </td>
                    <td className="py-4 px-6 text-gray-800">
                      After uploading a contract, click the &quot;Chat with AI&quot; button
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="w-full py-20 bg-black text-white">
        <div className="container px-4 md:px-6 mx-auto">
          <div className="flex flex-col items-center text-center max-w-3xl mx-auto">
            <div className="mb-8">
              <h2 className="text-4xl font-bold mb-6">
                Ready to Streamline Your Contract Analysis?
              </h2>
              <p className="text-xl text-gray-200 max-w-2xl mx-auto">
                Start extracting valuable insights from your contracts today
              </p>
            </div>
            
            <div className="flex flex-col sm:flex-row gap-4 w-full max-w-md mx-auto">
              <Link href="/contract" className="w-full">
                <Button className="w-full h-14 px-8 text-lg font-medium bg-white text-black hover:bg-gray-100 transition-all duration-200">
                  Get Started <ArrowRight className="ml-2 h-5 w-5" />
                </Button>
              </Link>
            </div>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="w-full py-8 bg-white border-t border-gray-200">
        <div className="container px-4 md:px-6 mx-auto">
          <div className="flex flex-col md:flex-row items-center justify-between">
            <p className="text-gray-800 mb-4 md:mb-0">
              © {new Date().getFullYear()} Contract Analysis System
            </p>
            <div className="flex space-x-8">
              <Link href="/contract" className="text-gray-800 hover:text-black transition-colors">
                Upload Contract
              </Link>
            </div>
          </div>
        </div>
      </footer>
    </div>
  );
}
