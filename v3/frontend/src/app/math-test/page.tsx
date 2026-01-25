'use client';

import InputCard from '@/components/lesson/math/InputCard';
import NumberLineCard from '@/components/lesson/math/NumberLineCard';
import MathRenderer from '@/components/lesson/math/MathRenderer';

export default function MathTestPage() {
    return (
        <div className="min-h-screen bg-[#0f0c29] text-white p-8 font-sans">
            <header className="max-w-4xl mx-auto mb-12 text-center">
                <h1 className="text-4xl font-bold bg-gradient-to-r from-cyan-400 to-purple-500 bg-clip-text text-transparent mb-4">
                    Math Engine V1.0 (Test)
                </h1>
                <p className="text-gray-400">
                    Prototypy komponentów do kursu matematyki (Klasa 7).
                    Wykorzystuje <code className="text-cyan-300">Katex</code> do renderowania wzorów.
                </p>
            </header>

            <main className="max-w-3xl mx-auto flex flex-col gap-12">

                {/* SECTION 1: Rendering Demo */}
                <section>
                    <h2 className="text-xl font-bold text-gray-300 mb-6 border-l-4 border-purple-500 pl-3">1. Wyświetlanie Wzorów (FormulaCard)</h2>
                    <div className="glass-card p-6 rounded-xl border border-white/10">
                        <p className="mb-4">Tekst z wplecionymi wzorami:</p>
                        <MathRenderer content={String.raw`
Pole trójkąta obliczamy ze wzoru: $$P = \frac{1}{2} a \cdot h$$

Gdzie:
*   $a$ - długość podstawy
*   $h$ - wysokość opuszczona na tę podstawę
                        `} />
                    </div>
                </section>

                {/* SECTION 2: Input Cards */}
                <section>
                    <h2 className="text-xl font-bold text-gray-300 mb-6 border-l-4 border-cyan-500 pl-3">2. Zadania Interaktywne (InputCard)</h2>

                    <div className="flex flex-col gap-8">
                        {/* Example 1: Simple Addition with formatting */}
                        <InputCard
                            question={String.raw`Ile to jest $2^3 + 4$?`}
                            correctAnswer="12"
                            hint="Pamiętaj o kolejności wykonywania działań. Najpierw potęgowanie."
                            explanation={String.raw`$$2^3 = 8$$, a następnie $$8 + 4 = 12$$. Proste!`}
                        />

                        {/* Example 2: Fractions */}
                        <InputCard
                            question={String.raw`Rozwiąż równanie: $\frac{1}{2}x = 10$`}
                            correctAnswer="20"
                            placeholder="x = ..."
                            explanation={String.raw`Aby pozbyć się ułamka, mnożymy obie strony przez 2. $$x = 10 \cdot 2 = 20$$.`}
                        />

                        {/* Example 3: Geometry with Units */}
                        <InputCard
                            question={String.raw`Oblicz pole kwadratu o boku $a = 6$ cm.`}
                            correctAnswer="36"
                            unit="cm^2"
                            placeholder="Pole"
                            explanation={String.raw`$$P = a^2 = 6^2 = 36$$.`}
                        />
                    </div>
                </section>

                {/* SECTION 3: Number Line */}
                <section>
                    <h2 className="text-xl font-bold text-gray-300 mb-6 border-l-4 border-yellow-500 pl-3">3. Oś Liczbowa (NumberLineCard)</h2>
                    <div className="flex flex-col gap-8">

                        <NumberLineCard
                            question={String.raw`Zaznacz na osi liczbę $1.5$`}
                            min={-2}
                            max={4}
                            step={1}
                            correctValue={1.5}
                            tolerance={0.2}
                            explanation={String.raw`Liczba $1.5$ leży dokładnie w połowie między $1$ a $2$.`}
                        />

                        <NumberLineCard
                            question={String.raw`Gdzie leży liczba ujemna $-3$?`}
                            min={-5}
                            max={0}
                            step={1}
                            correctValue={-3}
                            tolerance={0.2}
                        />

                        <NumberLineCard
                            question={String.raw`Zaznacz przybliżenie $\sqrt{2} \approx 1.4$`}
                            min={0}
                            max={3}
                            step={0.5}
                            correctValue={1.4}
                            tolerance={0.15}
                            explanation={String.raw`$\sqrt{2}$ to w przybliżeniu $1.41$, więc szukamy miejsca nieco przed $1.5$.`}
                        />

                    </div>
                </section>

            </main>
        </div>
    );
}
