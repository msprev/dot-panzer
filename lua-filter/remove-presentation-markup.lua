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

function Header(elem)
    text = pandoc.utils.stringify(elem)
    if text == "" then
        return {}
    end
    return pandoc.Header(1, elem.content, elem.attr)
end
