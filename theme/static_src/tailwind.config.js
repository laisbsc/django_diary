module.exports = {
    content: [
        '../templates/**/*.html',
        '../../templates/**/*.html',
        '../../**/templates/**/*.html',
    ],
    theme: {
        extend: {
            colors: {
                cream:        '#F2EBD5',
                amber:        '#E8A62C',
                sand:         '#D9C49C',
                sienna:       '#D98723',
                cobalt:       '#153FB3',
                ink:          '#1A1610',
                'ink-muted':  '#5C4F35',
                'ink-light':  '#9A8A6A',
            },
            fontFamily: {
                serif: ['Lora', 'Georgia', 'serif'],
                sans:  ['DM Sans', 'system-ui', 'sans-serif'],
            },
            typography: ({ theme }) => ({
                DEFAULT: {
                    css: {
                        color: theme('colors.ink-muted'),
                        fontSize: '15px',
                        lineHeight: '1.8',
                        a: { color: theme('colors.cobalt'), textDecoration: 'none' },
                        'a:hover': { textDecoration: 'underline' },
                        h1: { fontFamily: theme('fontFamily.serif').join(', '), color: theme('colors.ink') },
                        h2: { fontFamily: theme('fontFamily.serif').join(', '), color: theme('colors.ink') },
                        h3: { fontFamily: theme('fontFamily.serif').join(', '), color: theme('colors.ink') },
                        strong: { color: theme('colors.ink'), fontWeight: '500' },
                        blockquote: {
                            borderLeftColor: theme('colors.amber'),
                            borderLeftWidth: '3px',
                            backgroundColor: 'rgba(232,166,44,0.08)',
                            borderRadius: '0 2px 2px 0',
                            fontFamily: theme('fontFamily.serif').join(', '),
                            fontStyle: 'italic',
                            color: theme('colors.ink'),
                        },
                        'blockquote p': { margin: '0' },
                        code: { color: theme('colors.cobalt') },
                    },
                },
            }),
        },
    },
    plugins: [
        require('@tailwindcss/forms'),
        require('@tailwindcss/typography'),
        require('@tailwindcss/aspect-ratio'),
    ],
}
