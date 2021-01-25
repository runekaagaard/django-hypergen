events:
  id: input1    event: oninput  callback: autocomplete_items group: blockable throttle: 500
  id: textarea1 event: onchange callback: spellcheck         group: whenever  debounce: 1000
  id: button1   event: onclick  callback: save_data          group: save
timers:
  - callback: update_graph interval: 1200 group: whenever

execution_groups:
  whenever:
  blockable:
    blocks_for: [save]
  save:
    block_message: "Please wait until data is saved on the server"
    clears_before_block: [blockable]
  serial:
    sync: true

