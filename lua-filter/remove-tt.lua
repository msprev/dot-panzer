function Str(elem)
    text = pandoc.utils.stringify(elem)
    if text == "[TT]" then
        return {}
    end
end

