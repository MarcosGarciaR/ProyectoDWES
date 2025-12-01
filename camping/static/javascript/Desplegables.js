  document.addEventListener('DOMContentLoaded', function () {
    // toggles para los grupos principales
    document.querySelectorAll('.accordion-group').forEach(group => {
      const header = group.querySelector('.accordion-header');
      header.addEventListener('click', () => {
        group.classList.toggle('open');
      });
    });

    // toggles para subgrupos
    document.querySelectorAll('.subgroup').forEach(sub => {
      const header = sub.querySelector('.subgroup-header');
      header.addEventListener('click', () => {
        sub.classList.toggle('open');
      });
    });
  });