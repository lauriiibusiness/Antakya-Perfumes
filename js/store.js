/* ═══════════════════════════════════════════════
   ANTAKYA PERFUMES — Store, Cart & Account Logic
   ═══════════════════════════════════════════════ */

function fmtPrice(n) { return '€' + n.toFixed(2).replace('.', ','); }

// ── PRODUCT CATALOGUE ──────────────────────────────────────────
const PRODUCTS_DEFAULT = [
  {
    id:1, name:'Rouge Cristal', inspiredBy:'Baccarat Rouge 540',
    notes:'Saffron · Ambergris · Cedar · Jasmine',
    description:'An ethereal dance of saffron and jasmine wrapped in a warm amber haze. Rouge Cristal captures the iconic metallic-floral signature of the world\'s most coveted fragrance — clean, celestial, and utterly addictive. Longevity that carries you from morning to midnight.',
    price:42.99, volume:'50ml', image:'images/bottle-clean1.jpg',
    category:'unisex', badge:'Bestseller', isNew:false, available:true,
    season:'all-season', occasion:'date-night'
  },
  {
    id:2, name:'Oud Noir', inspiredBy:'Oud Wood',
    notes:'Oud · Rosewood · Vetiver · Sandalwood',
    description:'Deep as midnight, rich as ancient earth. Oud Noir opens with smoky rosewood before settling into a warm, resinous base of genuine oud and sandalwood. A fragrance for those who command presence and leave a trail that lingers long after they\'ve left the room.',
    price:42.99, volume:'50ml', image:'images/bottle-hero.jpg',
    category:'men', badge:null, isNew:false, available:true,
    season:'winter', occasion:'special'
  },
  {
    id:3, name:'Soir Noir', inspiredBy:'Black Orchid',
    notes:'Black Orchid · Truffle · Dark Chocolate · Patchouli',
    description:'Dark, seductive, and otherworldly. Black orchid and truffle intertwine with rich patchouli in a scent that defies convention. Soir Noir is worn by those who leave a lasting, unforgettable impression — bold, mysterious, and unmistakably luxurious.',
    price:42.99, volume:'50ml', image:'images/bottle-reflection.jpg',
    category:'unisex', badge:'New', isNew:true, available:true,
    season:'winter', occasion:'date-night'
  },
  {
    id:4, name:'Nuit Doré', inspiredBy:"La Nuit de L'Homme",
    notes:'Cardamom · Lavender · Cedarwood · Vetiver',
    description:'Aromatic, elegant, and undeniably masculine. Crisp lavender meets the warm spice of cardamom before giving way to a sensuous cedar and vetiver dry-down. The scent of a man who knows exactly who he is — refined, confident, and timeless.',
    price:42.99, volume:'50ml', image:'images/bottle-clean1.jpg',
    category:'men', badge:null, isNew:false, available:true,
    season:'all-season', occasion:'office'
  },
  {
    id:5, name:'Belle Minuit', inspiredBy:'Good Girl',
    notes:'Jasmine · Tuberose · Tonka Bean · Cocoa',
    description:'Feminine power, bottled. Lush tuberose and intoxicating jasmine are anchored by a rich tonka bean and cocoa base — a duality of light and darkness, playfulness and depth. Belle Minuit is the fragrance of a woman who writes her own rules.',
    price:42.99, volume:'50ml', image:'images/bottle-clean2.jpg',
    category:'women', badge:null, isNew:false, available:true,
    season:'all-season', occasion:'date-night'
  },
  {
    id:6, name:'Empire', inspiredBy:'Creed Aventus',
    notes:'Pineapple · Bergamot · Oakmoss · Birch · Musk',
    description:'Success has a scent. The opening burst of pineapple and bergamot gives way to a sophisticated heart of oakmoss and birch, finishing with a clean, powerful musk that lingers for hours. Empire is worn by those who lead, not follow.',
    price:42.99, volume:'50ml', image:'images/bottle-hero.jpg',
    category:'men', badge:'Limited', isNew:false, available:true,
    season:'all-season', occasion:'office'
  },
  {
    id:7, name:'Rose Noire', inspiredBy:'La Vie Est Belle',
    notes:'Rose · Iris · Praline · Patchouli',
    description:'A modern love story written in flowers and praline. Rose and iris bloom over a warm, decadent base of praline and patchouli — radiant, feminine, and impossible to forget. Rose Noire is joy made tangible, beauty made wearable.',
    price:42.99, volume:'50ml', image:'images/bottle-clean2.jpg',
    category:'women', badge:'New', isNew:true, available:true,
    season:'summer', occasion:'casual'
  },
  {
    id:8, name:'Velvet Amber', inspiredBy:'1 Million',
    notes:'Blood Orange · Cinnamon · Leather · Amber',
    description:'Bold, daring, and unapologetic. Blood orange and cinnamon ignite the senses before leather and amber create a warm, precious skin-like finish. Velvet Amber commands attention the moment you walk in — wear it and own the room.',
    price:42.99, volume:'50ml', image:'images/bottle-clean1.jpg',
    category:'men', badge:'New', isNew:true, available:true,
    season:'winter', occasion:'special'
  },
  {
    id:9, name:'Fleur Noir', inspiredBy:'Coco Mademoiselle',
    notes:'Orange · Rose · Patchouli · Vetiver',
    description:'A woman of contradictions. Fresh orange and floral rose give way to a deeply sensual patchouli and vetiver dry-down. Fleur Noir is the scent of effortless Parisian chic — spirited yet sophisticated, never predictable.',
    price:42.99, volume:'50ml', image:'images/bottle-clean2.jpg',
    category:'women', badge:null, isNew:false, available:true,
    season:'all-season', occasion:'office'
  },
  {
    id:10, name:'Velours Blanc', inspiredBy:'Molecule 01',
    notes:'Iso E Super · Musk · Cedarwood · Amber',
    description:'Minimalism elevated to art. This fascinatingly skin-reactive formula wraps around your natural scent, creating something entirely your own. Subtle yet magnetic — everyone will wonder what you\'re wearing, and no two people wear it the same.',
    price:42.99, volume:'50ml', image:'images/bottle-reflection.jpg',
    category:'unisex', badge:null, isNew:true, available:true,
    season:'all-season', occasion:'casual'
  },
  {
    id:11, name:'Or Noir', inspiredBy:'Sauvage Parfum',
    notes:'Bergamot · Sichuan Pepper · Ambroxan · Sandalwood',
    description:'Raw and noble. Bergamot and Sichuan pepper ignite a powerful opening before ambroxan creates that signature electrifying trail. Or Noir is masculine perfumery at its most iconic — wild at first, deeply sophisticated at its core.',
    price:42.99, volume:'50ml', image:'images/bottle-hero.jpg',
    category:'men', badge:null, isNew:false, available:true,
    season:'all-season', occasion:'casual'
  },
  {
    id:12, name:'Nuit de Soie', inspiredBy:'Chanel N°5',
    notes:'Ylang-Ylang · Rose · Sandalwood · Vetiver · Musk',
    description:'The fragrance that needs no introduction, reimagined. Ylang-ylang and rose create an opulent floral heart over a timeless sandalwood and vetiver base. Some fragrances transcend time — Nuit de Soie is one of them.',
    price:42.99, volume:'50ml', image:'images/bottle-clean2.jpg',
    category:'women', badge:null, isNew:false, available:true,
    season:'winter', occasion:'special'
  },
];

// Merge with any admin-saved overrides
function loadProducts() {
  const saved = localStorage.getItem('antakya_products');
  if (!saved) return PRODUCTS_DEFAULT;
  try {
    const overrides = JSON.parse(saved);
    // Merge: saved overrides win; new defaults are appended
    const merged = [...PRODUCTS_DEFAULT];
    overrides.forEach(op => {
      const idx = merged.findIndex(p => p.id === op.id);
      if (idx >= 0) merged[idx] = { ...merged[idx], ...op };
      else merged.push(op);
    });
    return merged;
  } catch(e) { return PRODUCTS_DEFAULT; }
}
let PRODUCTS = loadProducts();

// ── CART ───────────────────────────────────────────────────────
const Cart = {
  KEY: 'antakya_cart',
  load()      { return JSON.parse(localStorage.getItem(this.KEY) || '[]'); },
  save(items) { localStorage.setItem(this.KEY, JSON.stringify(items)); },

  add(productId, qty = 1) {
    const p = PRODUCTS.find(p => p.id === productId);
    if (!p || p.available === false) return;
    const items = this.load();
    const ex = items.find(i => i.id === productId);
    if (ex) ex.qty += qty;
    else items.push({ id:p.id, name:p.name, inspiredBy:p.inspiredBy, price:p.price, image:p.image, volume:p.volume, qty });
    this.save(items); this.refresh(); this.toast(p.name);
  },
  remove(id)  { this.save(this.load().filter(i => i.id !== id)); this.refresh(); },
  setQty(id, qty) {
    qty = parseInt(qty);
    if (qty <= 0) return this.remove(id);
    const items = this.load();
    const item  = items.find(i => i.id === id);
    if (item) item.qty = qty;
    this.save(items); this.refresh();
  },
  clear()  { this.save([]); this.refresh(); },
  count()  { return this.load().reduce((s,i) => s + i.qty, 0); },
  total()  { return this.load().reduce((s,i) => s + i.price * i.qty, 0); },

  open() {
    document.getElementById('cart-panel')?.classList.add('open');
    document.getElementById('cart-overlay')?.classList.add('show');
    document.body.style.overflow = 'hidden';
    this.renderPanel();
  },
  close() {
    document.getElementById('cart-panel')?.classList.remove('open');
    document.getElementById('cart-overlay')?.classList.remove('show');
    document.body.style.overflow = '';
  },
  refresh() {
    this.updateBadge();
    if (document.getElementById('cart-panel')?.classList.contains('open')) this.renderPanel();
    if (typeof renderCartPage === 'function') renderCartPage();
  },
  updateBadge() {
    const n = this.count();
    document.querySelectorAll('.cart-count').forEach(el => {
      el.textContent = n;
      el.classList.toggle('has-items', n > 0);
    });
  },
  renderPanel() {
    const items = this.load();
    const el    = document.getElementById('cart-items');
    if (!el) return;
    if (items.length === 0) {
      el.innerHTML = `
        <div class="cart-empty">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.2" width="48" height="48">
            <path d="M6 2L3 6v14a2 2 0 002 2h14a2 2 0 002-2V6l-3-4z"/>
            <line x1="3" y1="6" x2="21" y2="6"/>
            <path d="M16 10a4 4 0 01-8 0"/>
          </svg>
          <p>Your cart is empty</p>
          <a href="index.html#collection" class="btn-gold" style="margin-top:20px;font-size:.6rem;letter-spacing:.3em;padding:12px 28px;" onclick="Cart.close()">Shop Now</a>
        </div>`;
      document.getElementById('cart-footer').style.display = 'none';
      return;
    }
    el.innerHTML = items.map(item => `
      <div class="cart-item" data-id="${item.id}">
        <div class="cart-item-img"><img src="${item.image}" alt="${item.name}"></div>
        <div class="cart-item-body">
          <div class="cart-item-name">${item.name}</div>
          <div class="cart-item-sub">Inspired by ${item.inspiredBy}</div>
          <div class="cart-item-row">
            <div class="qty-ctrl">
              <button class="qty-btn" onclick="Cart.setQty(${item.id},${item.qty-1})">−</button>
              <span class="qty-val">${item.qty}</span>
              <button class="qty-btn" onclick="Cart.setQty(${item.id},${item.qty+1})">+</button>
            </div>
            <span class="cart-item-price">${fmtPrice(item.price * item.qty)}</span>
          </div>
        </div>
        <button class="cart-remove" onclick="Cart.remove(${item.id})">×</button>
      </div>`).join('');
    const total = this.total();
    document.getElementById('cart-total-val').textContent = fmtPrice(total);
    const rem = 60 - total;
    const dEl = document.getElementById('delivery-msg');
    if (dEl) {
      dEl.textContent = rem > 0 ? `Add ${fmtPrice(rem)} more for free delivery` : '✓ You qualify for free delivery!';
      dEl.classList.toggle('free', rem <= 0);
    }
    document.getElementById('cart-footer').style.display = 'block';
  },
  toast(name) {
    document.querySelector('.cart-toast')?.remove();
    const t = document.createElement('div');
    t.className = 'cart-toast';
    t.innerHTML = `<span class="toast-dot"></span><strong>${name}</strong> added to cart`;
    document.body.appendChild(t);
    requestAnimationFrame(() => t.classList.add('show'));
    setTimeout(() => { t.classList.remove('show'); setTimeout(() => t.remove(), 400); }, 2800);
  }
};

// ── ORDERS ─────────────────────────────────────────────────────
const Orders = {
  KEY: 'antakya_orders',
  load()       { return JSON.parse(localStorage.getItem(this.KEY) || '[]'); },
  save(orders) { localStorage.setItem(this.KEY, JSON.stringify(orders)); },
  place(buyer) {
    const items = Cart.load();
    if (!items.length) return false;
    const order = {
      id: 'ANT-' + Date.now(),
      date: new Date().toISOString(),
      buyer,
      items,
      subtotal: Cart.total(),
      total: Cart.total() >= 60 ? Cart.total() : Cart.total() + 3.99,
      delivery: Cart.total() >= 60 ? 'FREE' : '€3,99',
      status: 'pending'
    };
    const orders = this.load();
    orders.unshift(order);
    this.save(orders);
    Cart.clear();
    return order;
  },
  updateStatus(orderId, status) {
    const orders = this.load();
    const o = orders.find(x => x.id === orderId);
    if (o) { o.status = status; this.save(orders); }
  }
};

// ── ACCOUNT ────────────────────────────────────────────────────
const Account = {
  KEY:       'antakya_account',
  USERS_KEY: 'antakya_users',
  ADMIN_EMAIL: 'admin@antakyaperfumes.com',
  ADMIN_PASS:  'Antakya2025!',

  load()       { return JSON.parse(localStorage.getItem(this.KEY) || 'null'); },
  save(data)   { localStorage.setItem(this.KEY, JSON.stringify(data)); },
  isLoggedIn() { return !!this.load(); },
  isAdmin()    { const u = this.load(); return u && u.isAdmin === true; },
  get()        { return this.load(); },

  login(email, password) {
    if (email.toLowerCase() === this.ADMIN_EMAIL && password === this.ADMIN_PASS) {
      this.save({ id: 0, email: this.ADMIN_EMAIL, firstName: 'Admin', lastName: '', isAdmin: true });
      return { ok: true, admin: true };
    }
    const users = JSON.parse(localStorage.getItem(this.USERS_KEY) || '[]');
    const user  = users.find(u => u.email.toLowerCase() === email.toLowerCase());
    if (!user)                     return { ok: false, error: 'No account found with that email.' };
    if (user.password !== password) return { ok: false, error: 'Incorrect password.' };
    this.save({ id: user.id, email: user.email, firstName: user.firstName, lastName: user.lastName, membership: user.membership || false });
    return { ok: true, admin: false };
  },

  register({ firstName, lastName, email, password }) {
    const users = JSON.parse(localStorage.getItem(this.USERS_KEY) || '[]');
    if (users.find(u => u.email.toLowerCase() === email.toLowerCase()))
      return { ok: false, error: 'An account with this email already exists.' };
    const user = { id: Date.now(), firstName, lastName, email, password, membership: false };
    users.push(user);
    localStorage.setItem(this.USERS_KEY, JSON.stringify(users));
    this.save({ id: user.id, email: user.email, firstName, lastName, membership: false });
    return { ok: true };
  },

  joinMembership() {
    const s = this.load(); if (!s) return;
    const users = JSON.parse(localStorage.getItem(this.USERS_KEY) || '[]');
    const u = users.find(x => x.id === s.id);
    if (u) { u.membership = true; localStorage.setItem(this.USERS_KEY, JSON.stringify(users)); }
    s.membership = true; this.save(s);
  },
  cancelMembership() {
    const s = this.load(); if (!s) return;
    const users = JSON.parse(localStorage.getItem(this.USERS_KEY) || '[]');
    const u = users.find(x => x.id === s.id);
    if (u) { u.membership = false; localStorage.setItem(this.USERS_KEY, JSON.stringify(users)); }
    s.membership = false; this.save(s);
  },

  logout() { localStorage.removeItem(this.KEY); window.location.href = 'index.html'; },

  updateNavUI() {
    const user  = this.load();
    const label = document.querySelector('.account-label');
    if (label) label.textContent = user ? (user.isAdmin ? '⚙ Admin' : user.firstName) : '';
    document.querySelectorAll('.nav-account-icon').forEach(el => {
      el.title = user ? (user.isAdmin ? 'Admin Panel' : `Hello, ${user.firstName}`) : 'Login / Register';
      if (user?.isAdmin) el.href = 'admin.html';
    });
  }
};

// ── GLOBAL DOM INIT ────────────────────────────────────────────
document.addEventListener('DOMContentLoaded', () => {
  Cart.updateBadge();
  Account.updateNavUI();
  document.querySelectorAll('.open-cart').forEach(btn => btn.addEventListener('click', () => Cart.open()));
  document.getElementById('close-cart')?.addEventListener('click',   () => Cart.close());
  document.getElementById('cart-overlay')?.addEventListener('click', () => Cart.close());
  document.addEventListener('keydown', e => { if (e.key === 'Escape') Cart.close(); });
  const nav = document.getElementById('nav');
  if (nav) {
    const upd = () => nav.classList.toggle('scrolled', window.scrollY > 60);
    window.addEventListener('scroll', upd, { passive: true });
    upd();
  }
});
