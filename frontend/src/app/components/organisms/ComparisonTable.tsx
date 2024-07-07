"use client";
// "use client";

// import React from 'react';
// import { Card, Typography } from "@material-tailwind/react";
// import '../../../app/globals.css'

// interface SolutionData {
//     [parameter: string]: string | number | boolean;
//   }
  
// interface ComparisonTableProps {
//     solutionsData: { [solution: string]: SolutionData };
//     activeParameters: number[];
//   }

// export const ComparisonTable = ({activeParameters, solutionsData}: ComparisonTableProps) => {
//   return (
//     //@ts-ignore
//     <Card className="h-full w-full overflow-auto">
//        <div className="overflow-x-auto">
//         <table className="min-w-full table-auto text-left">
//           <thead>
//             <tr className='bg-gray-900'>
//               <th className="border-b border-gray-700 p-2 sm:p-4 md:p-5 lg:px-14 text-white font-bold leading-none opacity-70 font-source-code-pro">
//                 Solution Name
//               </th>
//               {activeParameters.map((head) => (
//                 <th
//                   key={head}
//                   className="border-b border-gray-700 p-2 sm:p-4 md:p-5 lg:px-14 text-white font-bold leading-none opacity-70 font-source-code-pro"
//                 >
//                   {head}
//                 </th>
//               ))}
//             </tr>
//           </thead>
//           <tbody>
//             {Object.entries(solutionsData).map(([solutionName, parameterValues], index) => {
//               const isLast = index === Object.entries(solutionsData).length - 1;
//               const classes = isLast ? "p-2 sm:p-4 md:p-5 lg:px-14" : "p-2 sm:p-4 md:p-5 lg:px-14 border-b border-gray-700";

//               return (
//                 <tr key={solutionName} className="bg-gray-800">
//                   <td className={classes}>
//                     {solutionName}
//                   </td>
//                   {activeParameters.map((parameter) => (
//                     <td key={parameter} className={classes}>
//                       {parameterValues[parameter] ?? 'N/A'}
//                     </td>
//                   ))}
//                 </tr>
//               );
//             })}
//           </tbody>
//         </table>
//       </div>
//   </Card>
//   );
// };

// export default ComparisonTable;

import React from 'react';
import { Card } from "@material-tailwind/react";
import '../../../app/globals.css';
import { useGlobalState } from "@/context/GlobalStateProvider";
import { getParameterNameById } from '@/app/utils/getParameterNameById';

interface SolutionData {
    [parameter: number]: string | number | boolean;
}

interface ComparisonTableProps {
    solutionsData: { [solution: string]: SolutionData };
    activeParameters: number[];
}

export const ComparisonTable: React.FC<ComparisonTableProps> = ({ activeParameters, solutionsData }) => {
  const { parameters } = useGlobalState();

  const getParameterName = (paramId: number) => {
    return getParameterNameById(parameters, paramId) || paramId.toString();
  };


  return (
    // @ts-ignore
    <Card className="h-full w-full overflow-auto">
       <div className="overflow-x-auto">
        <table className="min-w-full table-auto text-left">
          <thead>
            <tr className='bg-gray-900'>
              <th className="border-b border-gray-700 p-2 sm:p-4 md:p-5 lg:px-14 text-white font-bold leading-none opacity-70 font-source-code-pro">
                Solution Name
              </th>
              {activeParameters.map((paramId) => (
                <th
                  key={paramId}
                  className="border-b border-gray-700 p-2 sm:p-4 md:p-5 lg:px-14 text-white font-bold leading-none opacity-70 font-source-code-pro"
                >
                  {getParameterName(paramId)}
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {Object.entries(solutionsData).map(([solutionName, parameterValues], index) => {
              const isLast = index === Object.entries(solutionsData).length - 1;
              const classes = isLast ? "p-2 sm:p-4 md:p-5 lg:px-14" : "p-2 sm:p-4 md:p-5 lg:px-14 border-b border-gray-700";

              return (
                <tr key={solutionName} className="bg-gray-800">
                  <td className={classes}>
                    {solutionName}
                  </td>
                  {activeParameters.map((paramId) => (
                    <td key={paramId} className={classes}>
                      {parameterValues[paramId] ?? 'N/A'}
                    </td>
                  ))}
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>
    </Card>
  );
};

export default ComparisonTable;
