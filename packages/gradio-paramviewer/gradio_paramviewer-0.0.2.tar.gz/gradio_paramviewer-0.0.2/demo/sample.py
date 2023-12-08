docs = {
    "width": {
        "default": {
            "light": '<div class="highlight" style="background: #ffffff"><pre style="line-height: 125%;"><span></span><span style="color: #0000ff">None</span>\n</pre></div>',
            "dark": '<div class="highlight" style="background: #263238"><pre style="line-height: 125%;"><span></span><span style="color: #89DDFF">None</span>\n</pre></div>',
        },
        "type": {
            "light": '<div class="highlight" style="background: #ffffff"><pre style="line-height: 125%;"><span></span><span style="color: #000000">width</span>: <span style="color: #000000">int</span> | <span style="color: #0000ff">None</span>\n</pre></div>',
            "dark": '<div class="highlight" style="background: #263238"><pre style="line-height: 125%;"><span></span><span style="color: #EEFFFF">width</span><span style="color: #89DDFF">:</span> <span style="color: #82AAFF">int</span> <span style="color: #89DDFF">|</span> <span style="color: #89DDFF">None</span>\n</pre></div>',
        },
        "description": "Width of the displayed image in pixels.",
    },
    "type": {
        "default": {
            "light": '<div class="highlight" style="background: #ffffff"><pre style="line-height: 125%;"><span></span><span style="color: #55aa22">&quot;numpy&quot;</span>\n</pre></div>',
            "dark": '<div class="highlight" style="background: #263238"><pre style="line-height: 125%;"><span></span><span style="color: #C3E88D">&quot;numpy&quot;</span>\n</pre></div>',
        },
        "type": {
            "light": '<div class="highlight" style="background: #ffffff"><pre style="line-height: 125%;"><span></span><span style="color: #000000">type</span>: <span style="color: #55aa22">&quot;numpy&quot;</span> | <span style="color: #55aa22">&quot;pil&quot;</span> | <span style="color: #55aa22">&quot;filepath&quot;</span>\n</pre></div>',
            "dark": '<div class="highlight" style="background: #263238"><pre style="line-height: 125%;"><span></span><span style="color: #82AAFF">type</span><span style="color: #89DDFF">:</span> <span style="color: #C3E88D">&quot;numpy&quot;</span> <span style="color: #89DDFF">|</span> <span style="color: #C3E88D">&quot;pil&quot;</span> <span style="color: #89DDFF">|</span> <span style="color: #C3E88D">&quot;filepath&quot;</span>\n</pre></div>',
        },
        "description": 'The format the image is converted to before being passed into the prediction function. "numpy" converts the image to a numpy array with shape (height, width, 3) and values from 0 to 255, "pil" converts the image to a PIL image object, "filepath" passes a str path to a temporary file containing the image.',
    },
}
