import gradio as gr
from gradio_paramviewer import ParamViewer
from sample import docs

with gr.Blocks() as demo:
    gr.Markdown("## ParamViewer")
    ParamViewer(
        value=docs,
        label="Static",
    )


demo.launch()
