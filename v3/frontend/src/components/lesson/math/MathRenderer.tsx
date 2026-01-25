'use client';

import 'katex/dist/katex.min.css'; // Import KaTeX styles
import ReactMarkdown from 'react-markdown';
import remarkMath from 'remark-math';
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
                remarkPlugins={[remarkMath]}
                rehypePlugins={[rehypeKatex]}
                components={{
                    // Customize paragraph to not add extra margin if strictly inline context desired
                    p: ({ node, ...props }) => <p style={{ display: 'inline', margin: 0 }} {...props} />
                }}
            >
                {content}
            </ReactMarkdown>
        </div>
    );
}
