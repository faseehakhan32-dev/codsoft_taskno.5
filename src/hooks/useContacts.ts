import { useState, useEffect } from 'react';

export interface Contact {
  id: string;
  name: string;
  phone: string;
  email: string;
  address: string;
  createdAt: number;
}

export const useContacts = () => {
  const [contacts, setContacts] = useState<Contact[]>([]);
  const [loading, setLoading] = useState(true);

  // Load from localStorage on mount
  useEffect(() => {
    const saved = localStorage.getItem('contacts');
    if (saved) {
      try {
        setContacts(JSON.parse(saved));
      } catch (e) {
        console.error('Failed to parse contacts from localStorage', e);
      }
    }
    setLoading(false);
  }, []);

  // Save to localStorage whenever contacts change
  useEffect(() => {
    if (!loading) {
      localStorage.setItem('contacts', JSON.stringify(contacts));
    }
  }, [contacts, loading]);

  const addContact = (contact: Omit<Contact, 'id' | 'createdAt'>) => {
    const newContact: Contact = {
      ...contact,
      id: crypto.randomUUID(),
      createdAt: Date.now(),
    };
    setContacts((prev) => [...prev, newContact]);
    return newContact;
  };

  const updateContact = (id: string, updates: Partial<Omit<Contact, 'id' | 'createdAt'>>) => {
    setContacts((prev) =>
      prev.map((c) => (c.id === id ? { ...c, ...updates } : c))
    );
  };

  const deleteContact = (id: string) => {
    setContacts((prev) => prev.filter((c) => c.id !== id));
  };

  return {
    contacts,
    loading,
    addContact,
    updateContact,
    deleteContact,
  };
};
