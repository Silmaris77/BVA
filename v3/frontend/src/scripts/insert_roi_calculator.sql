-- Insert ROI Calculator
INSERT INTO tools (tool_id, title, description, tier, default_xp, config)
VALUES (
    'roi-calculator',
    'Kalkulator ROI',
    'Interaktywne narzędzie do obliczania zwrotu z inwestycji (ROI) oraz progu rentowności (BEP). Idealne do pokazywania wartości finansowej klientowi.',
    1,
    50,
    '{"inputs": ["price", "savings", "efficiency", "teamSize"]}'
);

-- Optional: Link to user if needed (usually handled by app logic on first use)
