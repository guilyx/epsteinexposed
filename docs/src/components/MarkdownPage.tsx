// Credits: Erwin Lejeune — 2026-02-22
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";

interface MarkdownPageProps {
  content: string;
}

export default function MarkdownPage({ content }: MarkdownPageProps) {
  return (
    <article className="md-prose">
      <ReactMarkdown remarkPlugins={[remarkGfm]}>{content}</ReactMarkdown>
    </article>
  );
}
