import React, { useEffect, useState, FC } from "react";
import styles from "./Accordion.module.css";

interface MAccordionProps {
  panel: string;
  data: Array<{ category: string; subcategories: string[] }>;
}

export const Accordion: FC<MAccordionProps> = ({ panel, data }) => {
  const [open, setOpen] = useState(0);
  const [noTransition, setNoTransition] = useState(true);

  const handleOpen = (value: number) => {
    if (value === 1 && open === 1) return;
    setOpen(open === value ? 0 : value);
  };

  const handleSubcategoryClick = (subcategory: string) => {
    console.log(`Subcategory clicked: ${subcategory}`);
  };

  useEffect(() => {
    const timer = setTimeout(() => {
      setNoTransition(false);
    }, 0);

    return () => clearTimeout(timer);
  }, []);

  return (
    <>
      {data.map((item, index) => (
        <div key={index} className={`accordion ${open === index + 1 ? styles.accordionOpen : ''} ${noTransition ? styles.noTransition : ''}`}>
          <div onClick={() => handleOpen(index + 1)} className={styles.Maccordion__accordion_header}>
            {item.category}
          </div>
          <div className={`${styles.Maccordion__accordion_body} ${open === index + 1 ? 'block' : 'hidden'}`}>
            {item.subcategories.map((sub, subIndex) => (
              <div
                key={subIndex}
                onClick={() => handleSubcategoryClick(sub)}
                className={styles.Maccordion__subcategory}
              >
                {sub}
              </div>
            ))}
          </div>
        </div>
      ))}
    </>
  );
};
