(function () {
  'use strict';

  var API_URL = '/api/lead';
  var modalRoot = null;
  var formEl = null;
  var statusEl = null;
  var lastFocus = null;

  function createModal() {
    if (document.getElementById('lead-modal')) {
      return;
    }

    var wrap = document.createElement('div');
    wrap.id = 'lead-modal';
    wrap.className = 'lead-modal';
    wrap.hidden = true;
    wrap.innerHTML =
      '<div class="lead-modal__backdrop" data-lead-close tabindex="-1"></div>' +
      '<div class="lead-modal__dialog" role="dialog" aria-modal="true" aria-labelledby="lead-modal-title">' +
      '  <button type="button" class="lead-modal__close" data-lead-close aria-label="Закрыть">×</button>' +
      '  <h2 id="lead-modal-title" class="lead-modal__title">Оставить заявку</h2>' +
      '  <p class="lead-modal__lead">Оставьте контакты — свяжусь удобным для вас способом.</p>' +
      '  <form class="lead-form" id="lead-form" novalidate>' +
      '    <label class="lead-form__field">' +
      '      <span>Имя</span>' +
      '      <input type="text" name="name" autocomplete="name" required maxlength="120">' +
      '    </label>' +
      '    <label class="lead-form__field">' +
      '      <span>Номер телефона</span>' +
      '      <input type="tel" name="phone" autocomplete="tel" required maxlength="40" inputmode="tel">' +
      '    </label>' +
      '    <label class="lead-form__field">' +
      '      <span>Желаемый способ связи</span>' +
      '      <select name="contact_method" required>' +
      '        <option value="" disabled selected>Выберите</option>' +
      '        <option value="Telegram">Telegram</option>' +
      '        <option value="Max">Max</option>' +
      '        <option value="Телефон">Телефон</option>' +
      '        <option value="WhatsApp">WhatsApp</option>' +
      '        <option value="Email">Email</option>' +
      '      </select>' +
      '    </label>' +
      '    <div class="lead-form__hp" aria-hidden="true">' +
      '      <label>Компания<input type="text" name="company" tabindex="-1" autocomplete="off"></label>' +
      '    </div>' +
      '    <p class="lead-form__status" id="lead-form-status" role="status" aria-live="polite"></p>' +
      '    <div class="lead-form__actions">' +
      '      <button type="submit" class="btn btn-primary">Отправить</button>' +
      '      <button type="button" class="btn btn-ghost" data-lead-close>Отмена</button>' +
      '    </div>' +
      '  </form>' +
      '</div>';

    document.body.appendChild(wrap);
    modalRoot = wrap;
    formEl = wrap.querySelector('#lead-form');
    statusEl = wrap.querySelector('#lead-form-status');

    wrap.querySelectorAll('[data-lead-close]').forEach(function (el) {
      el.addEventListener('click', closeModal);
    });

    formEl.addEventListener('submit', onSubmit);

    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && modalRoot && !modalRoot.hidden) {
        closeModal();
      }
    });
  }

  function openModal() {
    createModal();
    lastFocus = document.activeElement;
    modalRoot.hidden = false;
    modalRoot.setAttribute('aria-hidden', 'false');
    document.body.classList.add('lead-modal-open');
    statusEl.textContent = '';
    formEl.reset();
    var first = formEl.querySelector('input[name="name"]');
    if (first) {
      first.focus();
    }
  }

  function closeModal() {
    if (!modalRoot || modalRoot.hidden) {
      return;
    }
    modalRoot.hidden = true;
    modalRoot.setAttribute('aria-hidden', 'true');
    document.body.classList.remove('lead-modal-open');
    if (lastFocus && lastFocus.focus) {
      lastFocus.focus();
    }
  }

  function setStatus(message, isError) {
    statusEl.textContent = message;
    statusEl.classList.toggle('lead-form__status--error', !!isError);
  }

  function onSubmit(e) {
    e.preventDefault();
    if (!formEl.reportValidity()) {
      return;
    }

    var fd = new FormData(formEl);
    var payload = {
      name: String(fd.get('name') || '').trim(),
      phone: String(fd.get('phone') || '').trim(),
      contact_method: String(fd.get('contact_method') || '').trim(),
      company: String(fd.get('company') || '').trim(),
      page: window.location.pathname + window.location.hash,
    };

    var submitBtn = formEl.querySelector('button[type="submit"]');
    submitBtn.disabled = true;
    setStatus('Отправляем…', false);

    fetch(API_URL, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
    })
      .then(function (res) {
        return res.json().then(function (data) {
          return { res: res, data: data };
        });
      })
      .then(function (_ref) {
        var res = _ref.res;
        var data = _ref.data;
        if (res.ok && data.ok) {
          setStatus('Спасибо! Заявка отправлена — скоро свяжусь с вами.', false);
          formEl.reset();
          setTimeout(closeModal, 2200);
          return;
        }
        if (data.error === 'not_configured') {
          setStatus('Форма временно недоступна. Напишите в Telegram.', true);
          return;
        }
        if (data.error === 'validation') {
          setStatus('Проверьте имя, телефон и способ связи.', true);
          return;
        }
        if (data.error === 'invalid_token') {
          setStatus('Неверный TELEGRAM_BOT_TOKEN в .env — проверьте токен у @BotFather и перезапустите сервер (п. 2).', true);
          return;
        }
        if (data.error === 'invalid_chat') {
          setStatus('Неверный TELEGRAM_CHAT_ID — нужно число из getUpdates (message.chat.id), не @ник. Перезапустите сервер (п. 2).', true);
          return;
        }
        if (data.error === 'bot_blocked') {
          setStatus('Откройте вашего бота в Telegram и нажмите Start / напишите «привет», затем отправьте заявку снова.', true);
          return;
        }
        setStatus('Не удалось отправить. Проверьте .env и перезапустите сервер (manage.command → 2).', true);
      })
      .catch(function () {
        setStatus('Нет связи с сервером. Запустите сайт через server.py или напишите в Telegram.', true);
      })
      .finally(function () {
        submitBtn.disabled = false;
      });
  }

  document.addEventListener('click', function (e) {
    var trigger = e.target.closest('[data-lead-open]');
    if (trigger) {
      e.preventDefault();
      openModal();
    }
  });
})();
