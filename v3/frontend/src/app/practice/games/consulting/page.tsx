import { createClient } from '@/lib/supabase/server';
import { getGame } from '@/lib/games/consulting/actions';
import ConsultingGameLayout from './components/ConsultingGameLayout';
import { redirect } from 'next/navigation';

export const metadata = {
    title: 'Dream Team Consulting | BVA Academy',
    description: 'Manage your consulting firm, bid on contracts, and build your reputation.',
};

export default async function ConsultingGamePage() {
    const supabase = await createClient();
    const { data: { user } } = await supabase.auth.getUser();

    if (!user) {
        redirect('/login');
    }

    // Fetch or Create Game State
    const gameState = await getGame();

    return (
        <div className="h-screen w-full bg-black">
            <ConsultingGameLayout initialState={gameState}>
                {/* Layout handles the view switching internally */}
            </ConsultingGameLayout>
        </div>
    );
}
