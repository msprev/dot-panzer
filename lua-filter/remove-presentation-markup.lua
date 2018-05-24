-- Remove presentation markup for slides to prepare for printing

function HorizontalRule()
    return {}
end

function Para(elem)
    text = pandoc.utils.stringify(elem)
    if text == ". . ." then
        return {}
    end
end

function Image(elem)
    if elem.classes[1] == "handout" then
        return elem
    else
        return {}
    end
end

function Div(elem)
    if elem.classes[1] == "no-handout" then
        return {}
    else
        return elem
    end
end

function RawBlock(format, text)
    return {}
end

function Header(elem)
    text = pandoc.utils.stringify(elem)
    if text == "" then
        return {}
    end
    return pandoc.Header(1, elem.content, elem.attr)
end
