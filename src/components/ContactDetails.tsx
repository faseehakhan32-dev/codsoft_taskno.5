import React from 'react';
import type { Contact } from '../hooks/useContacts';
import { Phone, Mail, MapPin, Edit2, Trash2 } from 'lucide-react';

interface ContactDetailsProps {
  contact: Contact;
  onEdit: () => void;
  onDelete: () => void;
}

export const ContactDetails: React.FC<ContactDetailsProps> = ({ contact, onEdit, onDelete }) => {
  const initials = contact.name
    .split(' ')
    .map((n) => n[0] || '')
    .join('')
    .toUpperCase()
    .slice(0, 2);

  return (
    <div className="contact-details-container animate-fade-in">
      <div className="details-header">
        <div className="avatar-large">{initials}</div>
        <div className="header-info">
          <h2 className="details-name">{contact.name}</h2>
          <p className="details-creation-date">Added on {new Date(contact.createdAt).toLocaleDateString()}</p>
        </div>
        <div className="action-buttons">
          <button className="btn-icon btn-edit" title="Edit Contact" onClick={onEdit}>
            <Edit2 size={20} />
          </button>
          <button className="btn-icon btn-delete" title="Delete Contact" onClick={onDelete}>
            <Trash2 size={20} />
          </button>
        </div>
      </div>

      <div className="details-grid">
        <div className="detail-item">
          <div className="item-icon">
            <Phone size={18} />
          </div>
          <div className="item-content">
            <label className="item-label">Phone</label>
            <p className="item-value">{contact.phone}</p>
          </div>
        </div>

        <div className="detail-item">
          <div className="item-icon">
            <Mail size={18} />
          </div>
          <div className="item-content">
            <label className="item-label">Email</label>
            <p className="item-value">{contact.email || 'No email provided'}</p>
          </div>
        </div>

        <div className="detail-item full-width">
          <div className="item-icon">
            <MapPin size={18} />
          </div>
          <div className="item-content">
            <label className="item-label">Address</label>
            <p className="item-value">{contact.address || 'No address provided'}</p>
          </div>
        </div>
      </div>
    </div>
  );
};
