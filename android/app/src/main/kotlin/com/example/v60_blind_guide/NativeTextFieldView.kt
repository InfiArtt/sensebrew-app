package com.example.v60_blind_guide

import android.content.Context
import android.text.Editable
import android.text.InputType
import android.text.TextWatcher
import android.text.method.PasswordTransformationMethod
import android.view.KeyEvent
import android.view.View
import android.view.accessibility.AccessibilityNodeInfo
import android.view.inputmethod.EditorInfo
import android.view.inputmethod.InputMethodManager
import android.widget.EditText
import io.flutter.plugin.common.BinaryMessenger
import io.flutter.plugin.common.MethodChannel
import io.flutter.plugin.platform.PlatformView

class NativeTextFieldView(
    context: Context,
    viewId: Int,
    params: Map<*, *>,
    messenger: BinaryMessenger
) : PlatformView {

    private val editText: EditText = EditText(context)
    private val channel = MethodChannel(messenger, "sensebrew/nativetf_$viewId")

    init {
        val type = params["type"] as? String ?: "text"
        val label = params["label"] as? String ?: ""
        val initialValue = params["value"] as? String ?: ""
        val isPassword = params["isPassword"] as? Boolean ?: false

        editText.apply {
            isSingleLine = true
            imeOptions = EditorInfo.IME_ACTION_DONE
            
            // Only use hint for EditText to avoid confusing TalkBack with double descriptions
            hint = label

            setText(initialValue)
            setSelection(initialValue.length)

            textSize = 18f
            setPadding(24, 24, 24, 24)
            importantForAccessibility = View.IMPORTANT_FOR_ACCESSIBILITY_YES

            // Set inputType and transformationMethod LAST so they don't get reset by isSingleLine
            inputType = when {
                type == "number" -> InputType.TYPE_CLASS_NUMBER
                isPassword -> InputType.TYPE_CLASS_TEXT or InputType.TYPE_TEXT_VARIATION_PASSWORD
                else -> InputType.TYPE_CLASS_TEXT
            }

            if (isPassword) {
                transformationMethod = PasswordTransformationMethod.getInstance()
            }

            addTextChangedListener(object : TextWatcher {
                override fun beforeTextChanged(s: CharSequence?, start: Int, count: Int, after: Int) {}
                override fun onTextChanged(s: CharSequence?, start: Int, before: Int, count: Int) {}
                override fun afterTextChanged(s: Editable?) {
                    channel.invokeMethod("onChanged", s?.toString() ?: "")
                }
            })

            setOnEditorActionListener { v, actionId, event ->
                if (actionId == EditorInfo.IME_ACTION_DONE || (event != null && event.keyCode == KeyEvent.KEYCODE_ENTER && event.action == KeyEvent.ACTION_DOWN)) {
                    channel.invokeMethod("onDone", text?.toString() ?: "")
                    
                    // Hide the keyboard
                    val imm = context.getSystemService(Context.INPUT_METHOD_SERVICE) as InputMethodManager
                    imm.hideSoftInputFromWindow(v.windowToken, 0)
                    clearFocus()
                    
                    true
                } else false
            }
            
            setOnFocusChangeListener { _, hasFocus ->
                if (hasFocus) {
                    channel.invokeMethod("onFocused", null)
                }
            }

            accessibilityDelegate = object : View.AccessibilityDelegate() {
                override fun performAccessibilityAction(host: View, action: Int, args: android.os.Bundle?): Boolean {
                    if (action == AccessibilityNodeInfo.ACTION_ACCESSIBILITY_FOCUS) {
                        channel.invokeMethod("onAccessibilityFocused", null)
                    }
                    return super.performAccessibilityAction(host, action, args)
                }
            }
        }

        channel.setMethodCallHandler { call, result ->
            when (call.method) {
                "setValue" -> {
                    val newVal = call.argument<String>("value") ?: ""
                    editText.setText(newVal)
                    editText.setSelection(newVal.length)
                    result.success(null)
                }
                "setIsPassword" -> {
                    val isPwd = call.argument<Boolean>("isPassword") ?: false
                    if (isPwd) {
                        editText.inputType = InputType.TYPE_CLASS_TEXT or InputType.TYPE_TEXT_VARIATION_PASSWORD
                        editText.transformationMethod = PasswordTransformationMethod.getInstance()
                    } else {
                        editText.inputType = InputType.TYPE_CLASS_TEXT or InputType.TYPE_TEXT_FLAG_NO_SUGGESTIONS or InputType.TYPE_TEXT_VARIATION_VISIBLE_PASSWORD
                        editText.transformationMethod = null
                    }
                    editText.setSelection(editText.text.length)
                    result.success(null)
                }
                else -> result.notImplemented()
            }
        }
    }

    override fun getView(): View = editText

    override fun dispose() {
        channel.setMethodCallHandler(null)
    }
}
