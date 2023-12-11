CodeMirror.registerHelper("fold", "prefix", function(cm, start) {
    const line = start.line;
    const lineText = cm.getLine(line);

    // Check if this line contains a prefix and the previous line does not
    if (/^\s*(@prefix|PREFIX)/.test(lineText)) {
        if (line > 0 && /^\s*(@prefix|PREFIX)/.test(cm.getLine(line - 1))) {
            return null; // No fold range if the previous line also has a prefix
        }

        let end = line;
        while (end < cm.lastLine()) {
            end++;
            const nextLineText = cm.getLine(end);
            // Check if the line is blank (either empty or only containing whitespace)
            if (/^\s*$/.test(nextLineText)) {
                end--;  // Adjust end to the line before the blank line
                break;
            }
        }
        return {
            from: CodeMirror.Pos(line, lineText.length),
            to: CodeMirror.Pos(end, cm.getLine(end).length)
        };
    }
});
