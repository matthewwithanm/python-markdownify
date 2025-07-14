from markdownify import markdownify, LSTRIP, RSTRIP, STRIP

markdownify("<p>Hello</p>") == "Hello"  # test default of STRIP
markdownify("<p>Hello</p>", strip_document=LSTRIP) == "Hello\n\n"
markdownify("<p>Hello</p>", strip_document=RSTRIP) == "\n\nHello"
markdownify("<p>Hello</p>", strip_document=STRIP) == "Hello"
markdownify("<p>Hello</p>", strip_document=None) == "\n\nHello\n\n"
