function Div(el)
    if FORMAT == "latex" and el.classes[1] == "notes" then
        return {
            pandoc.Para({pandoc.RawInline("tex", "\\begin{callout}")}),
            el,
            pandoc.Para({pandoc.RawInline("tex", "\\end{callout}")})
        }
    end
end
