<title>НейроНика</title>
<style>
  @import url('https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,300;9..144,400;9..144,500;9..144,600&family=Fraunces:ital,opsz,wght@1,9..144,400;1,9..144,500&family=Manrope:wght@300;400;500;600;700&display=swap');

  :root{
    --bg: #1b1815;
    --panel: #241f1a;
    --panel-2: #2c261f;
    --ink: #f5efe4;
    --ink-dim: #b6ac9c;
    --ink-faint: #7d7566;
    --line: rgba(245,239,228,0.14);
    --line-soft: rgba(245,239,228,0.07);
    --gold: #c8a05f;

    --container: 1360px;
    --pad-in: clamp(1.25rem, 4vw, 4rem);

    color-scheme: dark;
  }

  @media (min-width: 1800px){
    :root{ --container: 1560px; }
    body{ font-size: 1.06rem; }
  }

  *, *::before, *::after{ box-sizing: border-box; }
  html{ scroll-behavior: smooth; }

  body{
    margin: 0;
    background: var(--bg);
    color: var(--ink);
    font-family: 'Manrope', system-ui, -apple-system, 'Segoe UI', sans-serif;
    font-weight: 400;
    line-height: 1.55;
    -webkit-font-smoothing: antialiased;
    overflow-x: hidden;
  }

  img, svg{ max-width: 100%; display: block; }
  a{ color: inherit; text-decoration: none; }

  ::selection{ background: var(--gold); color: #1b1815; }

  .container{
    width: 100%;
    max-width: var(--container);
    margin-inline: auto;
    padding-inline: var(--pad-in);
  }

  .eyebrow{
    font-family: 'Manrope', sans-serif;
    font-size: clamp(0.72rem, 0.68rem + 0.15vw, 0.8rem);
    font-weight: 600;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: var(--ink-faint);
  }

  h1, h2, h3{
    font-family: 'Fraunces', Georgia, 'Times New Roman', serif;
    font-weight: 500;
    line-height: 1.06;
    margin: 0;
    text-wrap: balance;
    letter-spacing: -0.01em;
  }
  em{
    font-style: italic;
    font-weight: 400;
    color: var(--gold);
  }

  p{ margin: 0; }

  a:focus-visible, button:focus-visible{
    outline: 2px solid var(--gold);
    outline-offset: 3px;
    border-radius: 2px;
  }

  /* ---------- header ---------- */
  .site-header{
    position: sticky;
    top: 0;
    z-index: 50;
    padding-top: env(safe-area-inset-top, 0px);
    background: rgba(27,24,21,0.72);
    backdrop-filter: blur(14px) saturate(120%);
    -webkit-backdrop-filter: blur(14px) saturate(120%);
    border-bottom: 1px solid var(--line-soft);
  }
  .site-header .container{
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 1rem;
    padding-block: 1rem;
  }
  .logo{
    font-family: 'Fraunces', serif;
    font-weight: 500;
    font-size: clamp(1.15rem, 1rem + 0.5vw, 1.4rem);
    white-space: nowrap;
  }
  .logo::after{ content: "."; color: var(--gold); }
  .nav-links{
    display: flex;
    align-items: center;
    gap: clamp(1.25rem, 3vw, 2.25rem);
  }
  .nav-link{
    font-size: 0.8rem;
    font-weight: 600;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: var(--ink-dim);
    padding-bottom: 3px;
    border-bottom: 1px solid transparent;
    transition: color 0.2s ease, border-color 0.2s ease;
  }
  .nav-link:hover{ color: var(--ink); border-color: var(--line); }
  @media (max-width: 420px){
    .nav-link--services{ display: none; }
  }

  .btn{
    display: inline-flex;
    align-items: center;
    justify-content: center;
    gap: 0.55em;
    font-family: 'Manrope', sans-serif;
    font-weight: 600;
    font-size: 0.85rem;
    letter-spacing: 0.03em;
    border-radius: 999px;
    padding: 0.85em 1.7em;
    border: 1px solid transparent;
    cursor: pointer;
    white-space: nowrap;
    transition: transform 0.25s cubic-bezier(.2,.8,.2,1), background 0.2s ease, border-color 0.2s ease, color 0.2s ease;
  }
  .btn-primary{
    background: var(--ink);
    color: #1b1815;
  }
  .btn-primary:hover{
    transform: translateY(-2px);
    background: #fff;
  }
  .btn-ghost{
    background: transparent;
    border-color: var(--line);
    color: var(--ink);
  }
  .btn-ghost:hover{
    border-color: var(--gold);
    color: var(--gold);
  }
  .btn-sm{ padding: 0.6em 1.3em; font-size: 0.76rem; }
  .btn svg{ width: 1em; height: 1em; flex-shrink: 0; }

  /* ---------- filmstrip ---------- */
  .filmstrip{
    display: flex;
    gap: clamp(0.5rem, 1.4vw, 1rem);
    overflow-x: auto;
    scroll-snap-type: x proximity;
    padding: clamp(0.9rem, 2vw, 1.5rem) var(--pad-in);
    scrollbar-width: none;
    -ms-overflow-style: none;
  }
  .filmstrip::-webkit-scrollbar{ display: none; }
  .film-tile{
    position: relative;
    flex: 0 0 auto;
    width: clamp(150px, 20vw, 260px);
    aspect-ratio: 3 / 4;
    border-radius: 4px;
    scroll-snap-align: start;
    background:
      radial-gradient(120% 90% at 20% 0%, rgba(245,239,228,0.07), transparent 60%),
      linear-gradient(155deg, var(--panel-2), var(--panel));
    overflow: hidden;
    display: flex;
    align-items: flex-end;
    padding: 0.9rem;
  }
  .film-tile::before{
    content: "";
    position: absolute;
    inset: 0;
    border: 1px solid var(--line-soft);
    border-radius: inherit;
    pointer-events: none;
  }
  .film-tag{
    font-size: 0.68rem;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: var(--ink-faint);
    display: flex;
    align-items: center;
    gap: 0.5em;
  }
  .film-tag svg{ width: 1.1em; height: 1.1em; opacity: 0.7; }

  /* ---------- hero ---------- */
  .hero{
    padding-block: clamp(1rem, 4vw, 2.5rem) clamp(3rem, 7vw, 5.5rem);
  }
  .hero-inner{
    max-width: 42rem;
    padding-top: clamp(2rem, 6vw, 4rem);
  }
  .hero .eyebrow{ display: block; margin-bottom: 1.1rem; }
  .hero h1{
    font-size: clamp(3rem, 6vw + 1rem, 5.6rem);
    margin-bottom: 0.4em;
  }
  .hero-lead{
    font-family: 'Fraunces', serif;
    font-style: italic;
    font-weight: 400;
    font-size: clamp(1.25rem, 1rem + 1vw, 1.75rem);
    color: var(--ink);
    max-width: 30ch;
    margin-bottom: 1.4rem;
    line-height: 1.28;
  }
  .hero-sub{
    font-size: clamp(0.95rem, 0.9rem + 0.2vw, 1.05rem);
    color: var(--ink-dim);
    max-width: 54ch;
    margin-bottom: 2.4rem;
  }
  .hero-actions{
    display: flex;
    flex-wrap: wrap;
    gap: 0.9rem;
  }

  /* ---------- section shell ---------- */
  section{ padding-block: clamp(3.5rem, 7vw, 6.5rem); }
  .section-head{
    display: flex;
    flex-direction: column;
    gap: 0.9rem;
    margin-bottom: clamp(2.5rem, 6vw, 4rem);
    max-width: 40rem;
  }
  .section-head h2{
    font-size: clamp(2rem, 1.5rem + 2.2vw, 3.1rem);
  }
  .section-head p{
    color: var(--ink-dim);
    font-size: clamp(1rem, 0.95rem + 0.2vw, 1.1rem);
    max-width: 46ch;
  }

  .services{
    border-top: 1px solid var(--line-soft);
    border-bottom: 1px solid var(--line-soft);
  }

  .services-grid{
    display: grid;
    grid-template-columns: 1fr;
    gap: clamp(2.25rem, 4vw, 3rem) clamp(1.5rem, 3vw, 2.5rem);
  }
  @media (min-width: 620px){ .services-grid{ grid-template-columns: repeat(2, 1fr); } }
  @media (min-width: 1000px){ .services-grid{ grid-template-columns: repeat(3, 1fr); } }
  @media (min-width: 1400px){ .services-grid{ grid-template-columns: repeat(4, 1fr); } }

  .card{ display: flex; flex-direction: column; }
  .card-photo{
    position: relative;
    aspect-ratio: 3 / 4;
    border-radius: 4px;
    overflow: hidden;
    margin-bottom: 1.25rem;
    background:
      radial-gradient(130% 100% at 15% 0%, rgba(245,239,228,0.06), transparent 55%),
      linear-gradient(160deg, var(--panel-2), var(--panel));
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    padding: 1rem;
    transition: transform 0.4s cubic-bezier(.2,.8,.2,1);
  }
  .card-photo::before{
    content: "";
    position: absolute;
    inset: 0;
    border: 1px solid var(--line-soft);
    border-radius: inherit;
    pointer-events: none;
  }
  .card:hover .card-photo{ transform: translateY(-3px); }
  .card-num{
    font-family: 'Fraunces', serif;
    font-style: italic;
    font-size: 1.1rem;
    color: var(--ink-faint);
    align-self: flex-end;
  }
  .card-hint{
    font-size: 0.7rem;
    letter-spacing: 0.06em;
    text-transform: uppercase;
    color: var(--ink-faint);
    display: flex;
    align-items: center;
    gap: 0.5em;
  }
  .card-hint svg{ width: 1.15em; height: 1.15em; opacity: 0.65; flex-shrink: 0; }
  .card h3{
    font-size: 1.3rem;
    font-weight: 500;
    margin-bottom: 0.5rem;
  }
  .card p{
    color: var(--ink-dim);
    font-size: 0.95rem;
    line-height: 1.58;
    max-width: 34ch;
  }

  /* ---------- contact ---------- */
  .contact-inner{
    display: flex;
    flex-direction: column;
    align-items: flex-start;
    gap: 1.6rem;
    padding-block: clamp(1rem, 3vw, 2rem);
  }
  .contact-inner h2{
    font-size: clamp(2.1rem, 1.6rem + 2.6vw, 3.4rem);
    max-width: 18ch;
  }
  .contact-inner > p{
    color: var(--ink-dim);
    max-width: 46ch;
    font-size: clamp(1rem, 0.95rem + 0.2vw, 1.1rem);
  }
  .contact-meta{
    display: flex;
    align-items: center;
    gap: 0.6rem;
    font-size: 0.85rem;
    letter-spacing: 0.04em;
    color: var(--ink-faint);
  }

  /* ---------- footer ---------- */
  footer{
    padding-block: 2.25rem;
    padding-bottom: calc(2.25rem + env(safe-area-inset-bottom, 0px));
    border-top: 1px solid var(--line-soft);
  }
  footer .container{
    display: flex;
    flex-wrap: wrap;
    align-items: center;
    justify-content: space-between;
    gap: 0.75rem;
  }
  .footer-brand{
    font-family: 'Fraunces', serif;
    font-weight: 500;
    font-size: 1rem;
  }
  .footer-note{
    color: var(--ink-faint);
    font-size: 0.82rem;
  }

  @media (prefers-reduced-motion: reduce){
    *{ animation: none !important; transition: none !important; }
  }
</style>

<svg style="display:none" aria-hidden="true">
  <defs>
    <symbol id="icon-camera" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
      <path d="M4 8h3l1.5-2h7L17 8h3a1 1 0 0 1 1 1v9a1 1 0 0 1-1 1H4a1 1 0 0 1-1-1V9a1 1 0 0 1 1-1z"/>
      <circle cx="12" cy="13" r="3.3"/>
    </symbol>
    <symbol id="icon-send" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round">
      <path d="M21 3L3 10.5l7 2.5m11-10l-5.5 17-5.5-6.5m11-10.5L10.5 13"/>
    </symbol>
  </defs>
</svg>

<header class="site-header">
  <div class="container">
    <a href="#top" class="logo">НейроНика</a>
    <nav class="nav-links">
      <a href="#services" class="nav-link nav-link--services">Услуги</a>
      <a href="https://t.me/che_nikaa" target="_blank" rel="noopener" class="btn btn-primary btn-sm">
        <svg viewBox="0 0 24 24"><use href="#icon-send"></use></svg>
        Написать
      </a>
    </nav>
  </div>
</header>

<main id="top">

  <div class="filmstrip" role="group" aria-label="Примеры работ">
    <div class="film-tile"><span class="film-tag"><svg viewBox="0 0 24 24"><use href="#icon-camera"></use></svg>работа 01</span></div>
    <div class="film-tile"><span class="film-tag"><svg viewBox="0 0 24 24"><use href="#icon-camera"></use></svg>работа 02</span></div>
    <div class="film-tile"><span class="film-tag"><svg viewBox="0 0 24 24"><use href="#icon-camera"></use></svg>работа 03</span></div>
    <div class="film-tile"><span class="film-tag"><svg viewBox="0 0 24 24"><use href="#icon-camera"></use></svg>работа 04</span></div>
    <div class="film-tile"><span class="film-tag"><svg viewBox="0 0 24 24"><use href="#icon-camera"></use></svg>работа 05</span></div>
    <div class="film-tile"><span class="film-tag"><svg viewBox="0 0 24 24"><use href="#icon-camera"></use></svg>работа 06</span></div>
  </div>

  <section class="hero">
    <div class="container">
      <div class="hero-inner">
        <span class="eyebrow">AI-креатор</span>
        <h1>НейроНика</h1>
        <p class="hero-lead">Контент, боты и цифровые продукты, созданные нейросетями</p>
        <p class="hero-sub">Работаю с брендами и предпринимателями: беру задачу целиком — от идеи и сценария до готового файла, ролика или продукта, который можно сразу публиковать или запускать.</p>
        <div class="hero-actions">
          <a href="#services" class="btn btn-primary">Смотреть услуги</a>
          <a href="https://t.me/che_nikaa" target="_blank" rel="noopener" class="btn btn-ghost">
            <svg viewBox="0 0 24 24"><use href="#icon-send"></use></svg>
            Написать в Telegram
          </a>
        </div>
      </div>
    </div>
  </section>

  <section class="services" id="services">
    <div class="container">
      <div class="section-head">
        <span class="eyebrow">Услуги</span>
        <h2>Чем я могу помочь</h2>
        <p>Восемь направлений — от контента для соцсетей до готового приложения. Каждое можно заказать отдельно или собрать в комплекс под вашу задачу.</p>
      </div>

      <div class="services-grid">

        <article class="card">
          <div class="card-photo">
            <span class="card-num">01</span>
            <span class="card-hint"><svg viewBox="0 0 24 24"><use href="#icon-camera"></use></svg>ваше фото</span>
          </div>
          <h3>Контент для брендов</h3>
          <p>Рекламные ролики, визуалы для соцсетей и промо-материалы, созданные нейросетями — быстро, без съёмочной группы и лишних смет.</p>
        </article>

        <article class="card">
          <div class="card-photo">
            <span class="card-num">02</span>
            <span class="card-hint"><svg viewBox="0 0 24 24"><use href="#icon-camera"></use></svg>ваше фото</span>
          </div>
          <h3>Мультфильмы</h3>
          <p>Анимационные истории и мультипликационные ролики: от сценария и персонажей до готовой озвученной анимации.</p>
        </article>

        <article class="card">
          <div class="card-photo">
            <span class="card-num">03</span>
            <span class="card-hint"><svg viewBox="0 0 24 24"><use href="#icon-camera"></use></svg>ваше фото</span>
          </div>
          <h3>Реалистичные видео</h3>
          <p>Фотореалистичные ролики и AI-актёры: оживляю фото, собираю кинематографичные сцены без камеры и локации.</p>
        </article>

        <article class="card">
          <div class="card-photo">
            <span class="card-num">04</span>
            <span class="card-hint"><svg viewBox="0 0 24 24"><use href="#icon-camera"></use></svg>ваше фото</span>
          </div>
          <h3>Нейро-примерка</h3>
          <p>Виртуальная примерка одежды на модели без съёмок, стилиста и шоурума — готовые фото образов за часы, а не дни.</p>
        </article>

        <article class="card">
          <div class="card-photo">
            <span class="card-num">05</span>
            <span class="card-hint"><svg viewBox="0 0 24 24"><use href="#icon-camera"></use></svg>ваше фото</span>
          </div>
          <h3>Telegram-боты</h3>
          <p>Боты для продаж, записи, автоворонок и поддержки клиентов — настраиваю логику под ваш процесс и запускаю под ключ.</p>
        </article>

        <article class="card">
          <div class="card-photo">
            <span class="card-num">06</span>
            <span class="card-hint"><svg viewBox="0 0 24 24"><use href="#icon-camera"></use></svg>ваше фото</span>
          </div>
          <h3>Контент-заводы</h3>
          <p>Системы автоматической генерации контента по шаблонам: десятки видео и постов в месяц без ручной работы.</p>
        </article>

        <article class="card">
          <div class="card-photo">
            <span class="card-num">07</span>
            <span class="card-hint"><svg viewBox="0 0 24 24"><use href="#icon-camera"></use></svg>ваше фото</span>
          </div>
          <h3>Создание сайтов</h3>
          <p>Лендинги, сайты-визитки и портфолио — быстрая загрузка и идеальный вид на любом экране, от телефона до телевизора.</p>
        </article>

        <article class="card">
          <div class="card-photo">
            <span class="card-num">08</span>
            <span class="card-hint"><svg viewBox="0 0 24 24"><use href="#icon-camera"></use></svg>ваше фото</span>
          </div>
          <h3>Создание приложений</h3>
          <p>Мобильные и веб-приложения под конкретную задачу — от идеи и интерфейса до рабочего продукта.</p>
        </article>

      </div>
    </div>
  </section>

  <section id="contact">
    <div class="container">
      <div class="contact-inner">
        <span class="eyebrow">Связь</span>
        <h2>Обсудим ваш <em>проект?</em></h2>
        <p>Расскажите, что нужно — подберу формат и покажу, как нейросети закроют задачу быстрее и дешевле привычного подхода.</p>
        <a href="https://t.me/che_nikaa" target="_blank" rel="noopener" class="btn btn-primary">
          <svg viewBox="0 0 24 24"><use href="#icon-send"></use></svg>
          Написать в Telegram
        </a>
        <p class="contact-meta">@che_nikaa</p>
      </div>
    </div>
  </section>
</main>

<footer>
  <div class="container">
    <span class="footer-brand">НейроНика.</span>
    <span class="footer-note">AI-контент, боты и продукты под ключ · 2026</span>
  </div>
</footer>