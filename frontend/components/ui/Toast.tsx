// components/ui/Toast.tsx

"use client";

import { useEffect } from "react";
import { CheckCircle, XCircle, AlertCircle, X } from "lucide-react";

interface ToastProps {
    message: string;
    type?: "success" | "error" | "info";
    isVisible: boolean;
    onClose: () => void;
    duration?: number;
}

export default function Toast({
    message,
    type = "success",
    isVisible,
    onClose,
    duration = 3000,
}: ToastProps) {
    useEffect(() => {
        if (isVisible && duration > 0) {
            const timer = setTimeout(onClose, duration);
            return () => clearTimeout(timer);
        }
    }, [isVisible, duration, onClose]);

    if (!isVisible) return null;

    const icons = {
        success: <CheckCircle className="w-5 h-5 text-green-600" />,
        error: <XCircle className="w-5 h-5 text-red-600" />,
        info: <AlertCircle className="w-5 h-5 text-blue-600" />,
    };

    const styles = {
        success: "bg-green-50 border-green-200 text-green-800",
        error: "bg-red-50 border-red-200 text-red-800",
        info: "bg-blue-50 border-blue-200 text-blue-800",
    };

    return (
        <div className="fixed top-4 right-4 z-50 animate-slide-in">
            <div
                className={`flex items-center gap-3 px-4 py-3 rounded-lg shadow-lg border ${styles[type]} min-w-[300px] max-w-md`}
            >
                {icons[type]}
                <p className="flex-1 text-sm font-medium">{message}</p>
                <button
                    onClick={onClose}
                    className="text-gray-500 hover:text-gray-700 transition"
                >
                    <X className="w-4 h-4" />
                </button>
            </div>
        </div>
    );
}