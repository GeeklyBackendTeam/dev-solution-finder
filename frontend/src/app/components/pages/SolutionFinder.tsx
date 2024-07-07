"use client";

// import { useState, useEffect } from "react";
// import { FunnelIcon, BriefcaseIcon } from "@heroicons/react/24/outline";
// import styles from "./SolutionFinder.module.css";
// import { Layout } from "../templates/Layout";
// import { ProjectList } from "../organisms/ProjectList";
// import { Accordion } from "../organisms/Accordion";
// import { useGlobalState } from "@/context/GlobalStateProvider";
// import { useParameterFilter } from "@/app/hooks/useParameterFilter";
// import ComparisonTable from "../organisms/ComparisonTable";

// var activeParams = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15];

var solutionsData = {
    "sol1": {
        1: true,
        2: "param 2",
        3: "param 3",
        4: 500,
        5: true,
        6: "param 2",
        7: "param 3",
        8: 100,
        9: "param 4",
        10: true,
        11: "param 2",
        12: "param 3",
        13: "param 4",
        14: "param 3",
        15: "param 4",
    },
    "sol14": {
        1: true,
        2: "param 2",
        3: "param 3",
        4: 500,
        5: true,
        6: "param 2",
        7: "param 3",
        8: 100,
        9: "param 4",
        10: true,
        11: "param 2",
        12: "param 3",
        13: "param 4",
        14: "param 3",
        15: "param 4",
    },
    "sol13": {
        1: true,
        2: "param 2",
        3: "param 3",
        4: 500,
        5: true,
        6: "param 2",
        7: "param 3",
        8: 100,
        9: "param 4",
        10: true,
        11: "param 2",
        12: "param 3",
        13: "param 4",
        14: "param 3",
        15: "param 4",
    },
    "sol12": {
        1: true,
        2: "param 2",
        3: "param 3",
        4: 500,
        5: true,
        6: "param 2",
        7: "param 3",
        8: 100,
        9: "param 4",
        10: true,
        11: "param 2",
        12: "param 3",
        13: "param 4",
        14: "param 3",
        15: "param 4",
    },
    "sol11": {
        1: true,
        2: "param 2",
        3: "param 3",
        4: 500,
        5: true,
        6: "param 2",
        7: "param 3",
        8: 100,
        9: "param 4",
        10: true,
        11: "param 2",
        12: "param 3",
        13: "param 4",
        14: "param 3",
        15: "param 4",
    },
    "sol10": {
        1: true,
        2: "param 2",
        3: "param 3",
        4: 500,
        5: true,
        6: "param 2",
        7: "param 3",
        8: 100,
        9: "param 4",
        10: true,
        11: "param 2",
        12: "param 3",
        13: "param 4",
        14: "param 3",
        15: "param 4",
    },
    "sol9": {
        1: true,
        2: "param 2",
        3: "param 3",
        4: 500,
        5: true,
        6: "param 2",
        7: "param 3",
        8: 100,
        9: "param 4",
        10: true,
        11: "param 2",
        12: "param 3",
        13: "param 4",
        14: "param 3",
        15: "param 4",
    },
    "sol8": {
        1: true,
        2: "param 2",
        3: "param 3",
        4: 500,
        5: true,
        6: "param 2",
        7: "param 3",
        8: 100,
        9: "param 4",
        10: true,
        11: "param 2",
        12: "param 3",
        13: "param 4",
        14: "param 3",
        15: "param 4",
    }                
}
// const Home = () => {
//   const {
//     isLeftPanelOpen,
//     setIsLeftPanelOpen,
//     isRightPanelOpen,
//     setIsRightPanelOpen,
//     currentProject,
//     parameters
//   } = useGlobalState();

//   const { selectedParameters, addParameter, removeParameter } = useParameterFilter();

//   useEffect(() => {
//     console.log("Selected Parameters: ", selectedParameters);
//   }, [selectedParameters]);

//   const data = [
//     {
//       category: "License",
//       subcategories: [{Name: "Parameter 1", Id: 1}, {Name: "Parameter 2", Id: 2}],
//     },
//     {
//       category: "Security",
//       subcategories: [{Name: "Parameter 1", Id: 3}, {Name: "Parameter 2", Id: 4}],
//     },
//     {
//       category: "Performance",
//       subcategories: [{Name: "Parameter 1", Id: 5}, {Name: "Parameter 2", Id: 6}],
//     },
//   ];

//   return (
//     <Layout>
//       <div className="relative flex h-screen w-full overflow-hidden">
//         <div
//           className={`flex flex-col bg-gray-900 text-gray-300 overflow-y-auto ${isLeftPanelOpen ? "w-1/5" : "w-0"}`}
//         >
//           <button
//             onClick={() => setIsLeftPanelOpen(!isLeftPanelOpen)}
//             className="absolute top-4 left-4 bg-gray-900 p-2 rounded"
//           >
//             <BriefcaseIcon className="h-6 w-6 text-purple-500" />
//           </button>
//           <div className={`w-full p-4 mt-16 ${isLeftPanelOpen ? 'block' : 'hidden'}`}>
//             <ProjectList />
//           </div>
//         </div>
//         <div
//           className={`flex-1 bg-gray-800 overflow-hidden ${
//             true ? 'transition-width duration-300' : ''
//           }`}
//         >
//           <div className="flex h-full items-center justify-center">
//           <ComparisonTable solutionsData={solutionsData} activeParameters={activeParams} />
//           </div>
//         </div>
//         <div
//           className={`flex flex-col bg-gray-900 text-gray-300 overflow-y-auto ${
//             true ? 'transition-width duration-300' : ''
//           } ${isRightPanelOpen ? "w-1/5" : "w-0"}`}
//         >
//           <button
//             onClick={() => setIsRightPanelOpen(!isRightPanelOpen)}
//             className="absolute top-4 right-4 bg-gray-900 p-2 rounded"
//           >
//             <FunnelIcon className="h-6 w-6 text-purple-500" />
//           </button>
//           <div className={`w-full p-4 mt-16 ${isRightPanelOpen ? 'block' : 'hidden'}`}>
//             <Accordion 
//             panel="right" 
//             data={parameters}
//             onSubcategoryClick={(subcategoryId: number) => {
//                 addParameter(subcategoryId);
//               }} />
//           </div>
//         </div>
//       </div>
//     </Layout>
//   );
// };

// export default Home;

import { useEffect } from "react";
import { FunnelIcon, BriefcaseIcon } from "@heroicons/react/24/outline";
import styles from "./SolutionFinder.module.css";
import { Layout } from "../templates/Layout";
import { ProjectList } from "../organisms/ProjectList";
import { Accordion } from "../organisms/Accordion";
import { useGlobalState } from "@/context/GlobalStateProvider";
import { useParameterFilter } from "@/app/hooks/useParameterFilter";
import ComparisonTable from "../organisms/ComparisonTable";

const Home = () => {
  const {
    isLeftPanelOpen,
    setIsLeftPanelOpen,
    isRightPanelOpen,
    setIsRightPanelOpen,
    parameters,
  } = useGlobalState();

  const { selectedParameters, addParameter, removeParameter } = useParameterFilter();

  const handleSubcategoryClick = (subcategoryId: number) => {
    if (selectedParameters.includes(subcategoryId)) {
      removeParameter(subcategoryId);
    } else {
      addParameter(subcategoryId);
    }
  };

  return (
    <Layout>
      <div className="relative flex h-screen w-full overflow-hidden">
        <div
          className={`flex flex-col bg-gray-900 text-gray-300 overflow-y-auto ${isLeftPanelOpen ? "w-1/5" : "w-0"}`}
        >
          <button
            onClick={() => setIsLeftPanelOpen(!isLeftPanelOpen)}
            className="absolute top-4 left-4 bg-gray-900 p-2 rounded"
          >
            <BriefcaseIcon className="h-6 w-6 text-purple-500" />
          </button>
          <div className={`w-full p-4 mt-16 ${isLeftPanelOpen ? 'block' : 'hidden'}`}>
            <ProjectList />
          </div>
        </div>
        <div
          className={`flex-1 bg-gray-800 overflow-hidden ${
            true ? 'transition-width duration-300' : ''
          }`}
        >
          <div className="flex h-full items-center justify-center">
            <ComparisonTable solutionsData={solutionsData} activeParameters={selectedParameters} />
          </div>
        </div>
        <div
          className={`flex flex-col bg-gray-900 text-gray-300 overflow-y-auto ${
            true ? 'transition-width duration-300' : ''
          } ${isRightPanelOpen ? "w-1/5" : "w-0"}`}
        >
          <button
            onClick={() => setIsRightPanelOpen(!isRightPanelOpen)}
            className="absolute top-4 right-4 bg-gray-900 p-2 rounded"
          >
            <FunnelIcon className="h-6 w-6 text-purple-500" />
          </button>
          <div className={`w-full p-4 mt-16 ${isRightPanelOpen ? 'block' : 'hidden'}`}>
            <Accordion 
              panel="right" 
              data={parameters}
              selectedParameters={selectedParameters}
              onSubcategoryClick={handleSubcategoryClick} />
          </div>
        </div>
      </div>
    </Layout>
  );
};

export default Home;

