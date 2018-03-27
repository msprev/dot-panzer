-- Add a line break between paragraphs
-- This is useful for output to MS Word as linebreaks separating paragraphs
-- as sometimes requested by publishers

function Para(elem)
  table.insert(elem.c, pandoc.LineBreak())
  return elem
end
