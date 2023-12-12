// The `Streamlit` object exists because our html file includes
// `streamlit-component-lib.js`.
// If you get an error about "Streamlit" not being defined, that
// means you're missing that file.

function sendValue(value) {
  Streamlit.setComponentValue(value)
}

function autoGrow(textarea) {
  textarea.style.height = 'auto';
  textarea.style.height = Math.max(_ini_frame_height_, Math.min(textarea.scrollHeight, _max_frame_height_)) + 'px';
  textarea.style.overflowY = 'hidden';

  _frame_height_ = parseInt(textarea.style.height, 10);

  console.log("autoGrow() called:", textarea.style.height, _ini_frame_height_, textarea.scrollHeight, _max_frame_height_);
}

/**
 * The component's render function. This will be called immediately after
 * the component is initially loaded, and then again every time the
 * component gets new data from Python.
 */
var _frame_height_ = 30;
var _ini_frame_height_ = 30;
var _max_frame_height_ = 200;
function onRender(event) {
  if(!window.rendered) {
    const {value, cols, height, max_height, submit_label, reset_label, font_family} = event.detail.args;

    _frame_height_ = height;
    _ini_frame_height_ = height
    _max_frame_height_ = max_height;

    const input = document.getElementById("input_box");
    input.cols = cols;
    input.style.height = height + 'px';
    input.style.fontFamily = font_family;
    if(value !== null && value !== undefined && value !== "") {
      input.value = value;
    }

    const btn_submit = document.getElementById("btn_submit");
    const btn_reset = document.getElementById("btn_reset");
    btn_submit.textContent = submit_label;
    btn_reset.textContent = reset_label;

    btn_submit.onclick = event => {
      sendValue({"submit": input.value, "height":_ini_frame_height_});
      if(on_change) 
        on_change({"submit": input.value, "height":_ini_frame_height_});
    }

    btn_reset.onclick = event => {
      input.value = "";
      input.style.height = _ini_frame_height_ + 'px';
      // input.style.height = _ini_frame_height_;
      sendValue({"reset": true, "height":_ini_frame_height_});
      if(on_change) 
        on_change({"reset": true, "height":_ini_frame_height_})
    }
    
    // input.onkeyup = event => sendValue(event.target.value);
    input.addEventListener('keydown', (event) => {
      if (event.key === 'Enter' && !event.shiftKey) {
        event.preventDefault();
        let height = parseInt(input.style.height);
        sendValue({"submit": input.value, "height": height});
        if(on_change) 
          on_change({"submit": input.value, "height": height});
      } else if (event.key === 'Enter' && event.shiftKey) {
        event.preventDefault();
        const start = input.selectionStart;
        const end = input.selectionEnd;
        const value = input.value;
        input.value = value.substring(0, start) + '\n' + value.substring(end);
        input.selectionStart = input.selectionEnd = start + 1;

        input.style.height = 'auto';
        input.style.height = input.scrollHeight + 'px';
        // input.style.height = input.scrollHeight

        sendValue({height: input.scrollHeight})
        if(on_change) 
          on_change({height: input.scrollHeight})
      }

      Streamlit.setFrameHeight(Math.min(_frame_height_, _max_frame_height_)+62)
    });

    window.rendered = true;
  }

  console.log("height", _ini_frame_height_, _frame_height_, _max_frame_height_)
  // Streamlit.setFrameHeight(Math.min(_frame_height_, _max_frame_height_)+62)
}

// Render the component whenever python send a "render event"
Streamlit.events.addEventListener(Streamlit.RENDER_EVENT, onRender)
// Tell Streamlit that the component is ready to receive events
Streamlit.setComponentReady()
// Render with the correct height, if this is a fixed-height component
// Streamlit.setFrameHeight(Math.min(_frame_height_, _max_frame_height_)+45)
Streamlit.setFrameHeight(Math.min(_frame_height_, _max_frame_height_)+62)
