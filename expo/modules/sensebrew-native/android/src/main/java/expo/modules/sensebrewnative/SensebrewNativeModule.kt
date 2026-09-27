package expo.modules.sensebrewnative

import expo.modules.kotlin.modules.Module
import expo.modules.kotlin.modules.ModuleDefinition

class SensebrewNativeModule : Module() {
  override fun definition() = ModuleDefinition {
    Name("SensebrewNative")

    View(NativeTextFieldView::class) {
      Events("onChangeText", "onSubmit", "onFocusChange")

      // Props are only recorded here and applied together in
      // OnViewDidUpdateProps, so a text update always sees the event count sent
      // with it, and the input type is rebuilt once rather than once per prop.
      Prop("value", "") { view: NativeTextFieldView, value: String -> view.value = value }
      Prop("mostRecentEventCount", 0) { view: NativeTextFieldView, count: Int -> view.mostRecentEventCount = count }
      Prop("hint", "") { view: NativeTextFieldView, hint: String -> view.hint = hint }
      Prop("keyboard", "text") { view: NativeTextFieldView, keyboard: String -> view.keyboard = keyboard }
      Prop("secure", false) { view: NativeTextFieldView, secure: Boolean -> view.secure = secure }
      Prop("multiline", false) { view: NativeTextFieldView, multiline: Boolean -> view.multiline = multiline }
      Prop("editable", true) { view: NativeTextFieldView, editable: Boolean -> view.editable = editable }
      Prop("returnKey", "done") { view: NativeTextFieldView, returnKey: String -> view.returnKey = returnKey }
      Prop("textAlign", "left") { view: NativeTextFieldView, align: String -> view.textAlign = align }
      Prop("fontSize", 16.0) { view: NativeTextFieldView, size: Double -> view.fontSize = size }
      Prop("textColor", "#000000") { view: NativeTextFieldView, color: String -> view.textColor = color }
      Prop("hintColor", "#9E9E9E") { view: NativeTextFieldView, color: String -> view.hintColor = color }

      OnViewDidUpdateProps { view: NativeTextFieldView -> view.applyProps() }
      OnViewDestroys { view: NativeTextFieldView -> view.release() }
    }
  }
}
