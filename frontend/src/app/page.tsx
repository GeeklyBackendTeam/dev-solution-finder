import Image from "next/image";
import { ButtonDefault } from "./components/shared/MaterialButton";
import Chart from "./components/stats/Chart";
import { ComparisonTable } from "./components/table/ComparisonTable";

export default function Home() {
  return (
    <main className="flex min-h-screen flex-col items-center justify-between p-24">
      <div className="mb-32 grid text-center lg:mb-0 lg:w-full lg:max-w-5xl lg:grid-cols-4 lg:text-left">
      <p className="m-0 max-w-[30ch] text-sm opacity-50">
            <ButtonDefault/>
           
          </p>
          
      </div>
      <div>
       <ComparisonTable/>
      </div>
    </main>
  );
}
