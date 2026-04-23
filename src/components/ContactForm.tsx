import React, { useState, useEffect } from 'react';
import type { Contact } from '../hooks/useContacts';
import { User, Phone, Mail, MapPin, Save, X } from 'lucide-react';

interface ContactFormProps {
  contact?: Contact; // If provided, we are editing
  onSubmit: (data: Omit<Contact, 'id' | 'createdAt'>) => void;
  onCancel: () => void;
}

export const ContactForm: React.FC<ContactFormProps> = ({ contact, onSubmit, onCancel }) => {
  const [formData, setFormData] = useState({
    name: '',
    phone: '',
    email: '',
    address: '',
  });

  useEffect(() => {
    if (contact) {
      setFormData({
        name: contact.name,
        phone: contact.phone,
        email: contact.email,
        address: contact.address,
      });
    }
  }, [contact]);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onSubmit(formData);
  };

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
  };

  return (
    <div className="form-overlay animate-fade-in">
      <div className="form-modal animate-slide-up">
        <div className="form-header">
          <h3 className="form-title">{contact ? 'Edit Contact' : 'New Contact'}</h3>
          <button className="btn-close" onClick={onCancel}>
            <X size={20} />
          </button>
        </div>

        <form onSubmit={handleSubmit} className="contact-form">
          <div className="input-field">
            <User size={18} className="input-icon" />
            <input
              type="text"
              name="name"
              placeholder="Full Name"
              required
              value={formData.name}
              onChange={handleChange}
              autoFocus
            />
          </div>

          <div className="input-field">
            <Phone size={18} className="input-icon" />
            <input
              type="tel"
              name="phone"
              placeholder="Phone Number"
              required
              value={formData.phone}
              onChange={handleChange}
            />
          </div>

          <div className="input-field">
            <Mail size={18} className="input-icon" />
            <input
              type="email"
              name="email"
              placeholder="Email Address"
              value={formData.email}
              onChange={handleChange}
            />
          </div>

          <div className="input-field">
            <MapPin size={18} className="input-icon" />
            <textarea
              name="address"
              placeholder="Physical Address"
              rows={3}
              value={formData.address}
              onChange={handleChange}
            />
          </div>

          <div className="form-actions">
            <button type="button" className="btn-secondary" onClick={onCancel}>
              Cancel
            </button>
            <button type="submit" className="btn-primary">
              <Save size={18} />
              {contact ? 'Save Changes' : 'Create Contact'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};
