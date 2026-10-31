/*
 * Tema claro/oscuro.
 * 1) Al cargar la página aplica el tema guardado (o el del sistema operativo)
 *    lo antes posible, para evitar un destello del tema equivocado.
 * 2) Expone las funciones de los clientside callbacks registrados en app.py.
 */
(function () {
  // dcc.Store con storage_type="local" guarda el valor en JSON bajo su id
  var CLAVE = "theme-store";

  function temaGuardado() {
    try {
      var valor = JSON.parse(window.localStorage.getItem(CLAVE));
      return valor === "light" || valor === "dark" ? valor : null;
    } catch (e) {
      return null;
    }
  }

  function temaDelSistema() {
    return window.matchMedia &&
      window.matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light";
  }

  function aplicarTema(tema) {
    document.documentElement.setAttribute("data-bs-theme", tema === "dark" ? "dark" : "light");
  }

  // Aplicación inmediata al cargar
  aplicarTema(temaGuardado() || temaDelSistema());

  window.dash_clientside = Object.assign({}, window.dash_clientside, {
    tema: {
      // Clic en el botón -> nuevo valor del Store.
      // En la carga inicial (sin clics) guarda el tema ya aplicado si el Store está vacío.
      alternar: function (nClicks, guardado) {
        var actual = document.documentElement.getAttribute("data-bs-theme") || "light";
        if (!nClicks) {
          return guardado === "light" || guardado === "dark"
            ? window.dash_clientside.no_update
            : actual;
        }
        return actual === "dark" ? "light" : "dark";
      },

      // Store -> atributo data-bs-theme y textos accesibles del botón
      aplicar: function (tema) {
        tema = tema === "dark" ? "dark" : "light";
        aplicarTema(tema);
        var texto = tema === "dark" ? "Cambiar a modo claro" : "Cambiar a modo oscuro";
        return [texto, texto];
      }
    }
  });
})();
