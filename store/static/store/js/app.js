/**
 * Veylora E-Commerce — Client-side JavaScript
 */

document.addEventListener('DOMContentLoaded', () => {
  // 1. Mobile navigation drawer toggle
  const mobileToggle = document.getElementById('mobileMenuToggle');
  const mobileDrawer = document.getElementById('mobileDrawer');
  const drawerBackdrop = document.getElementById('drawerBackdrop');
  const drawerCloseBtn = document.getElementById('drawerCloseBtn');

  function openDrawer() {
    if (mobileDrawer && drawerBackdrop) {
      mobileDrawer.classList.add('open');
      drawerBackdrop.classList.add('open');
      document.body.style.overflow = 'hidden';
      if (mobileToggle) mobileToggle.setAttribute('aria-expanded', 'true');
    }
  }

  function closeDrawer() {
    if (mobileDrawer && drawerBackdrop) {
      mobileDrawer.classList.remove('open');
      drawerBackdrop.classList.remove('open');
      document.body.style.overflow = '';
      if (mobileToggle) mobileToggle.setAttribute('aria-expanded', 'false');
    }
  }

  if (mobileToggle) {
    mobileToggle.addEventListener('click', openDrawer);
  }

  if (drawerCloseBtn) {
    drawerCloseBtn.addEventListener('click', closeDrawer);
  }

  if (drawerBackdrop) {
    drawerBackdrop.addEventListener('click', closeDrawer);
  }

  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && mobileDrawer && mobileDrawer.classList.contains('open')) {
      closeDrawer();
    }
  });

  // 2. Alert message close handlers & auto-dismiss
  const alerts = document.querySelectorAll('.alert');
  alerts.forEach(alert => {
    const closeBtn = alert.querySelector('.alert-close');
    if (closeBtn) {
      closeBtn.addEventListener('click', () => {
        alert.style.opacity = '0';
        setTimeout(() => alert.remove(), 250);
      });
    }

    // Auto-dismiss after 6 seconds
    setTimeout(() => {
      if (document.body.contains(alert)) {
        alert.style.opacity = '0';
        setTimeout(() => alert.remove(), 250);
      }
    }, 6000);
  });

  // 3. Product Quantity Stepper Controls
  const steppers = document.querySelectorAll('.quantity-control');
  steppers.forEach(stepper => {
    const btnMinus = stepper.querySelector('.qty-minus');
    const btnPlus = stepper.querySelector('.qty-plus');
    const input = stepper.querySelector('.qty-input');

    if (btnMinus && btnPlus && input) {
      const min = parseInt(input.getAttribute('min') || '1', 10);
      const max = parseInt(input.getAttribute('max') || '999', 10);

      btnMinus.addEventListener('click', () => {
        let val = parseInt(input.value || '1', 10);
        if (val > min) {
          input.value = val - 1;
          input.dispatchEvent(new Event('change'));
        }
      });

      btnPlus.addEventListener('click', () => {
        let val = parseInt(input.value || '1', 10);
        if (val < max) {
          input.value = val + 1;
          input.dispatchEvent(new Event('change'));
        }
      });
    }
  });
});
