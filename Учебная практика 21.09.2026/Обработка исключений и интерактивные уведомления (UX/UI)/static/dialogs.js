(function () {
  function snapshot(form) {
    Array.from(form.elements).forEach(function (el) {
      if (!el.name || el.type === "hidden" || el.type === "submit" || el.type === "button") {
        return;
      }
      el.dataset.initial = el.value;
    });
  }

  function isDirty(form) {
    return Array.from(form.elements).some(function (el) {
      if (el.dataset.initial === undefined) {
        return false;
      }
      return el.value !== el.dataset.initial;
    });
  }

  function closeBox(box) {
    if (box) {
      box.hidden = true;
    }
  }

  function openBox(box) {
    if (box) {
      box.hidden = false;
    }
  }

  function bindMessageBox(box) {
    if (!box) {
      return;
    }
    box.querySelectorAll("[data-action='ok']").forEach(function (btn) {
      btn.addEventListener("click", function () {
        closeBox(box);
      });
    });
    box.querySelectorAll("[data-action='no']").forEach(function (btn) {
      btn.addEventListener("click", function () {
        closeBox(box);
      });
    });
    box.querySelectorAll("[data-action='yes']").forEach(function (btn) {
      btn.addEventListener("click", function () {
        window.location.href = box.dataset.href || "/";
      });
    });
  }

  function warnIfDirty(event, href) {
    var form = document.querySelector(".partner-form");
    var box = document.getElementById("unsaved-warning");
    if (!form || !box || !isDirty(form)) {
      window.location.href = href;
      return;
    }
    event.preventDefault();
    box.dataset.href = href;
    openBox(box);
  }

  document.addEventListener("DOMContentLoaded", function () {
    var form = document.querySelector(".partner-form");
    if (form) {
      snapshot(form);
    }
    document.querySelectorAll(".message-box-overlay").forEach(bindMessageBox);
    document.querySelectorAll(".js-cancel").forEach(function (btn) {
      btn.addEventListener("click", function (event) {
        warnIfDirty(event, btn.dataset.href || "/");
      });
    });
    document.querySelectorAll(".js-back").forEach(function (link) {
      link.addEventListener("click", function (event) {
        warnIfDirty(event, link.getAttribute("href") || "/");
      });
    });
  });
})();
