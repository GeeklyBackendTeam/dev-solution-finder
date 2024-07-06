"use client";
import { useState, useEffect } from "react";
import { FunnelIcon, BriefcaseIcon } from "@heroicons/react/24/outline";
import styles from "./Home.module.css"; // Create this file for Home-specific styles if needed
import { Layout } from "./components/templates/Layout";
import { ProjectList } from "./components/organisms/ProjectList";
import { Accordion } from "./components/organisms/Accordion";

const Home = () => {
  const [leftPanelVisible, setLeftPanelVisible] = useState(true);
  const [rightPanelVisible, setRightPanelVisible] = useState(true);
  const [initialLoad, setInitialLoad] = useState(false);

  useEffect(() => {
    setInitialLoad(true);
  }, []);

  const data = [
    {
      category: "License",
      subcategories: [
        "Parameter 1",
        "Parameter 2",
      ],
    },
    {
      category: "Security",
      subcategories: [
        "Parameter 1",
        "Parameter 2",
      ],
    },
    {
      category: "Performance",
      subcategories: [
        "Parameter 1",
        "Parameter 2",
      ],
    },
  ];

  return (
    <Layout>
      <div className="relative flex h-screen w-full overflow-hidden">
        <div
          className={`flex flex-col bg-gray-900 text-gray-300 overflow-y-auto ${
            initialLoad ? 'transition-width duration-300' : ''
          } ${leftPanelVisible ? "w-1/5" : "w-0"}`}
        >
          <button
            onClick={() => setLeftPanelVisible(!leftPanelVisible)}
            className="absolute top-4 left-4 bg-gray-900 p-2 rounded"
          >
            <BriefcaseIcon className="h-6 w-6 text-purple-500" />
          </button>
          <div className={`w-full p-4 mt-16 ${leftPanelVisible ? 'block' : 'hidden'}`}>
            <ProjectList />
          </div>
        </div>
        <div
          className={`flex-1 bg-gray-800 overflow-hidden ${
            initialLoad ? 'transition-width duration-300' : ''
          }`}
        >
          <div className="flex h-full items-center justify-center">
           
          </div>
        </div>
        <div
          className={`flex flex-col bg-gray-900 text-gray-300 overflow-y-auto ${
            initialLoad ? 'transition-width duration-300' : ''
          } ${rightPanelVisible ? "w-1/5" : "w-0"}`}
        >
          <button
            onClick={() => setRightPanelVisible(!rightPanelVisible)}
            className="absolute top-4 right-4 bg-gray-900 p-2 rounded"
          >
            <FunnelIcon className="h-6 w-6 text-purple-500" />
          </button>
          <div className={`w-full p-4 mt-16 ${rightPanelVisible ? 'block' : 'hidden'}`}>
            <Accordion panel="right" data={data} />
          </div>
        </div>
      </div>
    </Layout>
  );
};

export default Home;
