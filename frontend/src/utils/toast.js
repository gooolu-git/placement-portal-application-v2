export const toast = {
  success(title, message = '', duration = 4000) {
    this._trigger('success', title, message, duration)
  },
  error(title, message = '', duration = 5000) {
    this._trigger('error', title, message, duration)
  },
  warning(title, message = '', duration = 4000) {
    this._trigger('warning', title, message, duration)
  },
  info(title, message = '', duration = 3000) {
    this._trigger('info', title, message, duration)
  },
  
  _trigger(type, title, message, duration) {
    const event = new CustomEvent('show-notification', {
      detail: { type, title, message, duration }
    })
    window.dispatchEvent(event)
  }
}