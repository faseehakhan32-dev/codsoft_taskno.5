import React from 'react';
import type { Contact } from '../hooks/useContacts';

interface ContactCardProps {
  contact: Contact;
  active: boolean;
  onClick: () => void;
}

export const ContactCard: React.FC<ContactCardProps> = ({ contact, active, onClick }) => {
  const initials = contact.name
    .split(' ')
    .map((n) => n[0])
    .join('')
    .toUpperCase()
    .slice(0, 2);

  return (
    <div
      className={`sidebar-contact-card ${active ? 'active' : ''}`}
      onClick={onClick}
    >
      <div className="avatar-small">
        {initials}
      </div>
      <div className="contact-info-small">
        <h4 className="contact-name-small">{contact.name}</h4>
        <p className="contact-phone-small">{contact.phone}</p>
      </div>
    </div>
  );
};
