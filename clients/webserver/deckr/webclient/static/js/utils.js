var PassVars = (function() {
  var loaded_vars = {};
  var loaded = false;

  function loadVars(vars) {
    if (loaded) return;
    loaded_vars = vars;
    loaded = true;
  }

  function getVars() {
    return loaded_vars;
  }

  return {
    getVars: getVars,
    loadVars: loadVars
  };
})();
