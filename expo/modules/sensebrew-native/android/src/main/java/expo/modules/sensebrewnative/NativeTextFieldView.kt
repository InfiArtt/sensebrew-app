package expo.modules.sensebrewnative

import android.content.Context
import android.graphics.Color
import android.os.Build
import android.text.Editable
import android.text.InputType
import android.text.TextWatcher
import android.text.method.PasswordTransformationMethod
import android.util.TypedValue
import android.view.Gravity
import android.view.KeyEvent
import android.view.View
import android.view.accessibility.AccessibilityEvent
import android.view.ViewGroup
import android.view.inputmethod.EditorInfo
import android.view.inputmethod.InputMethodManager
import android.widget.EditText
import android.widget.LinearLayout
import expo.modules.kotlin.AppContext
import expo.modules.kotlin.viewevent.EventDispatcher
import expo.modules.kotlin.views.ExpoView

/**
 * A plain Android EditText, named by its hint.
 *
 * React Native's own TextInput is an EditText too, but ReactEditText is made
 * not focusable in touch mode so that only JavaScript can move focus. Screen
 * readers always run in touch mode, so TalkBack and Jieshuo could not give the
 * field input focus, and cursor actions such as "go to start" / "go to end"
 * did nothing. This is the Flutter build's NativeTextFieldView.kt again: an
 * EditText left as Android ships it, which is what WhatsApp and TeamTalk use.
 *
 * The field's name is its hint, never a contentDescription: a
 * contentDescription makes screen readers treat it as a label rather than
 * editable text, and the editing actions disappear.
 */
class NativeTextFieldView(context: Context, appContext: AppContext) : ExpoView(context, appContext) {
  // A getter rather than a stored value: ExpoView reads this from requestLayout,
  // which Android already calls while the superclass is being constructed.
  override val shouldUseAndroidLayout: Boolean
    get() = true

  val onChangeText by EventDispatcher()
  val onSubmit by EventDispatcher()
  val onFocusChange by EventDispatcher()

  // Props, applied together in applyProps().
  var value = ""
  var mostRecentEventCount = 0
  var hint = ""

  /** "text", "number", "decimal" or "password". */
  var keyboard = "text"

  /** For keyboard "password": whether the characters are hidden. */
  var secure = false
  var multiline = false
  var editable = true

  /**
   * Select the whole value on focus, so typing replaces it while the value
   * itself stays in the field and is still read out.
   */
  var selectAllOnFocus = false

  /** "done" or "send". */
  var returnKey = "done"

  /** "left" or "center". */
  var textAlign = "left"
  var fontSize = 16.0
  var textColor = "#000000"
  var hintColor = "#9E9E9E"

  private val editText = EditText(context)

  /** Text changes the user made, so JS can say which of them it has seen. */
  private var eventCount = 0
  private var isSettingTextFromJs = false
  private var appliedInputConfig: String? = null

  init {
    // The wrapper is layout only; the EditText is the one accessibility node.
    importantForAccessibility = View.IMPORTANT_FOR_ACCESSIBILITY_NO
    editText.importantForAccessibility = View.IMPORTANT_FOR_ACCESSIBILITY_YES

    // The React Native wrapper around this view draws the border and fill.
    editText.background = null
    val horizontal = dp(12)
    editText.setPadding(horizontal, dp(8), horizontal, dp(8))

    addView(
      editText,
      LinearLayout.LayoutParams(ViewGroup.LayoutParams.MATCH_PARENT, ViewGroup.LayoutParams.MATCH_PARENT)
    )

    editText.addTextChangedListener(object : TextWatcher {
      override fun beforeTextChanged(s: CharSequence?, start: Int, count: Int, after: Int) = Unit
      override fun onTextChanged(s: CharSequence?, start: Int, before: Int, count: Int) = Unit
      override fun afterTextChanged(s: Editable?) {
        if (isSettingTextFromJs) return
        eventCount += 1
        onChangeText(mapOf("text" to (s?.toString() ?: ""), "eventCount" to eventCount))
      }
    })

    editText.setOnEditorActionListener { _, actionId, event ->
      val isEnter = event != null &&
        event.keyCode == KeyEvent.KEYCODE_ENTER &&
        event.action == KeyEvent.ACTION_DOWN
      val isAction = actionId == EditorInfo.IME_ACTION_DONE ||
        actionId == EditorInfo.IME_ACTION_SEND
      if (!multiline && (isAction || isEnter)) {
        onSubmit(mapOf("text" to editText.text.toString()))
        hideKeyboardAndBlur()
        true
      } else {
        false
      }
    }

    editText.setOnFocusChangeListener { _, hasFocus ->
      onFocusChange(mapOf("focused" to hasFocus))
    }
  }

  fun applyProps() {
    editText.hint = hint
    editText.setSelectAllOnFocus(selectAllOnFocus)
    editText.isEnabled = editable
    editText.setTextSize(TypedValue.COMPLEX_UNIT_SP, fontSize.toFloat())
    parseColor(textColor)?.let { editText.setTextColor(it) }
    parseColor(hintColor)?.let { editText.setHintTextColor(it) }

    val horizontalGravity = if (textAlign == "center") Gravity.CENTER_HORIZONTAL else Gravity.START
    val verticalGravity = if (multiline) Gravity.TOP else Gravity.CENTER_VERTICAL
    editText.gravity = horizontalGravity or verticalGravity

    applyInputConfig()

    // A text from JS only wins once JS has seen every change the user made;
    // otherwise a keystroke still on its way to JS would be overwritten by the
    // older value JS is holding.
    val current = editText.text.toString()
    if (mostRecentEventCount >= eventCount && value != current) {
      isSettingTextFromJs = true
      editText.setText(value)
      editText.setSelection(value.length)
      isSettingTextFromJs = false
      // Tell the screen reader the field's text changed, so it never keeps
      // announcing a copy of the field from before the change.
      editText.sendAccessibilityEvent(AccessibilityEvent.TYPE_WINDOW_CONTENT_CHANGED)
    }
  }

  /**
   * Input type, line mode and IME action. Only rebuilt when they change:
   * setting the input type restarts the keyboard and can move the cursor.
   */
  private fun applyInputConfig() {
    val config = "$keyboard|$secure|$multiline|$returnKey"
    if (config == appliedInputConfig) return
    appliedInputConfig = config

    val selection = editText.selectionEnd.coerceAtLeast(0)

    // Line mode first: setSingleLine resets the input type and transformation.
    editText.setSingleLine(!multiline)
    if (multiline) {
      editText.maxLines = Int.MAX_VALUE
      editText.imeOptions = EditorInfo.IME_ACTION_NONE
    } else {
      editText.imeOptions =
        if (returnKey == "send") EditorInfo.IME_ACTION_SEND else EditorInfo.IME_ACTION_DONE
    }

    var type = when (keyboard) {
      "number" -> InputType.TYPE_CLASS_NUMBER
      "decimal" -> InputType.TYPE_CLASS_NUMBER or InputType.TYPE_NUMBER_FLAG_DECIMAL
      // A revealed password stays a password field for the keyboard, so it
      // offers no suggestions and learns nothing from it.
      "password" -> if (secure) {
        InputType.TYPE_CLASS_TEXT or InputType.TYPE_TEXT_VARIATION_PASSWORD
      } else {
        InputType.TYPE_CLASS_TEXT or
          InputType.TYPE_TEXT_VARIATION_VISIBLE_PASSWORD or
          InputType.TYPE_TEXT_FLAG_NO_SUGGESTIONS
      }
      else -> InputType.TYPE_CLASS_TEXT or InputType.TYPE_TEXT_FLAG_CAP_SENTENCES
    }
    if (multiline) type = type or InputType.TYPE_TEXT_FLAG_MULTI_LINE
    editText.inputType = type
    editText.transformationMethod =
      if (keyboard == "password" && secure) PasswordTransformationMethod.getInstance() else null

    editText.setSelection(selection.coerceAtMost(editText.text.length))
  }

  private fun hideKeyboardAndBlur() {
    val imm = context.getSystemService(Context.INPUT_METHOD_SERVICE) as InputMethodManager
    imm.hideSoftInputFromWindow(editText.windowToken, 0)
    clearFocusWithoutRefocus()
  }

  /**
   * Up to Android 9, clearing focus in touch mode hands it to the first
   * focusable view, which would be the next text field and would bring the
   * keyboard back. React Native works around it the same way.
   */
  private fun clearFocusWithoutRefocus() {
    val root = rootView as? ViewGroup
    if (Build.VERSION.SDK_INT > Build.VERSION_CODES.P || !isInTouchMode || root == null) {
      editText.clearFocus()
      return
    }
    val previous = root.descendantFocusability
    root.descendantFocusability = ViewGroup.FOCUS_BLOCK_DESCENDANTS
    editText.clearFocus()
    root.descendantFocusability = previous
  }

  fun release() {
    if (editText.hasFocus()) hideKeyboardAndBlur()
  }

  private fun dp(value: Int): Int =
    TypedValue.applyDimension(TypedValue.COMPLEX_UNIT_DIP, value.toFloat(), resources.displayMetrics).toInt()

  private fun parseColor(color: String): Int? =
    try {
      Color.parseColor(color)
    } catch (e: IllegalArgumentException) {
      null
    }
}
