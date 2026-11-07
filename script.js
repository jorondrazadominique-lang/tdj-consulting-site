document.getElementById('year').textContent = new Date().getFullYear();

const form = document.getElementById('contact-form');
if (form) {
  form.addEventListener('submit', function (e) {
    e.preventDefault();
    const name = form.name.value.trim();
    const email = form.email.value.trim();
    const phone = form.phone.value.trim();
    const subject = form.subject.value;
    const lieu = form.lieu.value.trim();
    const delai = form.delai.value.trim();
    const message = form.message.value.trim();

    const mailSubject = `TDJ Consulting — ${subject} — ${name}`;
    const bodyLines = [
      `Nom : ${name}`,
      `Email : ${email}`,
      phone ? `Téléphone : ${phone}` : null,
      `Type de demande : ${subject}`,
      lieu ? `Lieu du projet : ${lieu}` : null,
      delai ? `Échéance souhaitée : ${delai}` : null,
      '',
      message
    ].filter(Boolean);

    const mailto = `mailto:jorondrazadominique@gmail.com?subject=${encodeURIComponent(mailSubject)}&body=${encodeURIComponent(bodyLines.join('\n'))}`;
    window.location.href = mailto;

    const note = document.getElementById('form-note');
    if (note) {
      note.textContent = 'Votre application mail devrait s\'ouvrir avec le message prêt à envoyer. Rien ne s\'est passé ? Écrivez directement à jorondrazadominique@gmail.com.';
    }
  });
}
