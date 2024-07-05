"use client"

import React from 'react';
import { Button, ButtonProps } from '@material-tailwind/react';

type CustomSize = 'icon';

interface MaterialButtonComponentProps {
  variant?: ButtonProps['variant'] | 'ghost';
  size?: ButtonProps['size'] | CustomSize;
  className?: string;
  onClick?: () => void;
  children: React.ReactNode;
  placeholder?: string;
  onPointerEnterCapture?: (event: MouseEvent) => void;
  onPointerLeaveCapture?: (event: MouseEvent) => void;
}

const MButton: React.FC<MaterialButtonComponentProps> = ({
  variant,
  size,
  className,
  onClick,
  children,
  ...rest
}) => {
  const buttonClasses = `${className ?? ''} ${
    variant === 'ghost' ? 'bg-transparent text-primary border-primary' : ''
  } ${size === 'icon' ? 'p-2 min-w-0' : ''}`;
return <></>
  // return (
    // <Button
    //   children={undefined} placeholder={undefined} onPointerEnterCapture={undefined} onPointerLeaveCapture={undefined} variant={variant === 'ghost' ? 'outlined' : variant}
    //   size={size !== 'icon' ? size : undefined}
    //   className={buttonClasses}
    //   onClick={onClick}
    //   {...rest}>
    //     Hello
    // </Button>

{/* <Button variant="text" loading={true} {...rest}>
  {children}
</Button> */}
  // );
};

export default MButton;
