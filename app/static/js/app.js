/* ============================================================
   Sistema Clínica Veterinaria — Minimal JS
   ============================================================ */

// Sidebar toggle (mobile)
document.addEventListener('DOMContentLoaded', function () {
  const sidebar = document.getElementById('sidebar');
  const backdrop = document.getElementById('sidebarBackdrop');
  const toggler = document.getElementById('sidebarToggler');

  function openSidebar() {
    sidebar.classList.add('show');
    backdrop.classList.add('show');
  }

  function closeSidebar() {
    sidebar.classList.remove('show');
    backdrop.classList.remove('show');
  }

  if (toggler) toggler.addEventListener('click', openSidebar);
  if (backdrop) backdrop.addEventListener('click', closeSidebar);

  // Close sidebar on link click (mobile)
  document.querySelectorAll('.sidebar-link').forEach(function (link) {
    link.addEventListener('click', function () {
      if (window.innerWidth < 992) closeSidebar();
    });
  });

  // Auto-dismiss flash messages after 5 seconds
  document.querySelectorAll('.alert-dismissible').forEach(function (alert) {
    setTimeout(function () {
      var bsAlert = bootstrap.Alert.getOrCreateInstance(alert);
      bsAlert.close();
    }, 5000);
  });
});

// Delete confirmation
function confirmarEliminar(nombre, url) {
  if (confirm('¿Está seguro de que desea eliminar "' + nombre + '"? Esta acción no se puede deshacer.')) {
    window.location.href = url;
  }
}
