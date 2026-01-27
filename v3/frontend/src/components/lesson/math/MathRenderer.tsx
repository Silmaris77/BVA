'use client';

import 'katex/dist/katex.min.css'; // Import KaTeX styles
import ReactMarkdown from 'react-markdown';
import remarkMath from 'remark-math';
import remarkGfm from 'remark-gfm';
import rehypeKatex from 'rehype-katex';

interface MathRendererProps {
    content: string; // The text containing LaTeX, e.g., "Calculate $2+2$"
    className?: string;
    inline?: boolean;
}

export default function MathRenderer({ content, className, inline }: MathRendererProps) {
    // If inline is strictly true, we might want to force it, but react-markdown handles $ vs $$ automatically.
    // Single $ = inline, Double $$ = block.

    return (
        <div className={`math-renderer ${className || ''} text-white`}>
            <ReactMarkdown
                remarkPlugins={[remarkMath, remarkGfm]}
                rehypePlugins={[rehypeKatex]}
                components={{
                    // Customize paragraph to not add extra margin if strictly inline context desired
                    p: ({ node, ...props }) => {
                        if (inline) return <span {...props} />
                        return <p className="mb-4" {...props} />
                    },
                    table: ({ node, ...props }) => <div className="overflow-x-auto my-4"><table className="w-full border-collapse border border-white/20 text-sm" {...props} /></div>,
                    thead: ({ node, ...props }) => <thead className="bg-white/10" {...props} />,
                    tbody: ({ node, ...props }) => <tbody {...props} />,
                    tr: ({ node, ...props }) => <tr className="border-b border-white/10" {...props} />,
                    th: ({ node, ...props }) => <th className="border border-white/20 px-4 py-3 text-left font-bold text-white/90" {...props} />,
                    td: ({ node, ...props }) => <td className="border border-white/20 px-4 py-3 text-white/80" {...props} />,
                    ul: ({ node, ...props }) => <ul className="list-disc pl-6 mb-4 space-y-1" {...props} />,
                    ol: ({ node, ...props }) => <ol className="list-decimal pl-6 mb-4 space-y-1" {...props} />,
                    li: ({ node, ...props }) => <li className="pl-1" {...props} />,
                }}
            >
                {content}
            </ReactMarkdown>
        </div>
    );
}
