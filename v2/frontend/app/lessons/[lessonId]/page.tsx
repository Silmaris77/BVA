import { LessonPlayer } from "@/components/lessons/LessonPlayer";

interface PageProps {
    params: Promise<{ lessonId: string }>;
}

export default async function LessonPage({ params }: PageProps) {
    const { lessonId } = await params;
    return <LessonPlayer lessonId={lessonId} />;
}
