"use client"
import Image from "next/image";
import { useState } from "react";
import { FunnelIcon, BriefcaseIcon } from '@heroicons/react/24/outline'

export default function Home() {
  const [leftPanelVisible, setLeftPanelVisible] = useState(true);
  const [rightPanelVisible, setRightPanelVisible] = useState(true);

  return (
    <main className="flex min-h-screen flex-col items-center justify-between p-0 m-0">
      <div className="flex h-screen w-full overflow-hidden">
        <div
          className={`flex flex-col items-center justify-center bg-gray-800 text-primary-foreground overflow-y-auto transition-width duration-300 ${
            leftPanelVisible ? 'w-1/5' : 'w-0'
          }`}
        >
          <button
            onClick={() => setLeftPanelVisible(!leftPanelVisible)}
            className="absolute top-4 left-4 bg-white p-2 rounded"
          >
             <BriefcaseIcon className="size-6 text-blue-500" />
          </button>

          {leftPanelVisible && (
            <div className="space-y-4">
              {/* Add any content here */}
            </div>
          )}
        </div>
        <div
          className={`flex-1 bg-gray-100 overflow-hidden transition-width duration-300 ${
            leftPanelVisible && rightPanelVisible ? 'mx-4' : leftPanelVisible || rightPanelVisible ? 'mx-2' : 'mx-0'
          }`}
        >
          <div className="flex h-full items-center justify-center">
            <h1 className="text-4xl font-bold">Main Content</h1>
          </div>
        </div>
        <div
          className={`flex flex-col items-center justify-center bg-gray-300 text-secondary-foreground overflow-y-auto transition-width duration-300 ${
            rightPanelVisible ? 'w-1/5' : 'w-0'
          }`}
        >
         
          <button
            onClick={() => setRightPanelVisible(!rightPanelVisible)}
            className="absolute top-4 right-4 bg-white p-2 rounded"
          >
             <FunnelIcon className="size-6 text-blue-500" />
          </button>
          {rightPanelVisible && (
            <div className="space-y-4">
              {/* Add any content here */}
            </div>
          )}
        </div>
      </div>
    </main>
  );
}
