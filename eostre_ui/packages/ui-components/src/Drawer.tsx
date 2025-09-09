"use client";

import { X } from "lucide-react";
import { motion, AnimatePresence } from "framer-motion";
import React from "react";
import clsx from "clsx";

interface DrawerProps {
    isOpen: boolean;
    onClose: () => void;
    title?: string;
    side?: "left" | "right" | "bottom";
    variant?: "nav" | "detail" | "form";
    className?: string;
    children: React.ReactNode;
}

export function Drawer({
    isOpen,
    onClose,
    title,
    side = "right",
    variant = "detail",
    className,
    children,
}: DrawerProps) {

    const sideClasses: Record<string, string> = {
        right: "top-[64px] right-0 h-[calc(100%-64px)] w-96",
        left: "top-[64px] left-0 h-[calc(100%-64px)] w-48",
        bottom: "bottom-0 left-0 w-full h-1/2",
    };

    const variantClasses: Record<NonNullable<DrawerProps["variant"]>, string> = {
        nav: "bg-brand-primary text-brand-light",
        detail: "bg-brand-light text-brand-dark dark:bg-brand-dark dark:text-brand-light",
        form: "bg-brand-light text-brand-dark dark:bg-brand-dark dark:text-brand-light",
    };

    return (
        <AnimatePresence>
            {isOpen && (
                <>
                    {/* Overlay (starts below the navbar) */}
                    <motion.div
                        className="fixed inset-0 top-12 bg-black/40 dark:bg-black/60 z-40"
                        initial={{ opacity: 0 }}
                        animate={{ opacity: 1 }}
                        exit={{ opacity: 0 }}
                        onClick={onClose}
                    />

                    {/* Drawer panel */}
                    <motion.div
                        className={clsx(
                            "fixed shadow-xl z-50 flex flex-col",
                            sideClasses[side],
                            variantClasses[variant],
                            className
                        )}
                        initial={{
                            x: side === "right" ? "100%" : side === "left" ? "-100%" : 0,
                            y: side === "bottom" ? "100%" : 0,
                        }}
                        animate={{ x: 0, y: 0 }}
                        exit={{
                            x: side === "right" ? "100%" : side === "left" ? "-100%" : 0,
                            y: side === "bottom" ? "100%" : 0,
                        }}
                        transition={{ type: "tween", duration: 0.3 }}
                    >
                        {/* Header */}
                        <div className="flex items-center justify-between border-b px-4 py-2">
                            {title && <h2 className="text-lg font-semibold">{title}</h2>}
                            <button 
                              onClick={onClose} 
                              aria-label="Close drawer"
                              className="p-1 rounded hover:bg-black/10 dark:hover:bg-white/10 focus:outline-none focus:ring-2 focus:ring-offset-1 focus:ring-brand-primary"
                            >
                                <X className="h-5 w-5" />
                            </button>
                        </div>

                        {/* Content */}
                        <div className="flex-1 overflow-y-auto p-4">{children}</div>
                    </motion.div>
                </>
            )}
        </AnimatePresence>
    );
}
