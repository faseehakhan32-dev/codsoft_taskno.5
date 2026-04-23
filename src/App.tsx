import React, { useState, useMemo } from 'react';
import { useContacts } from './hooks/useContacts';
import type { Contact } from './hooks/useContacts';
import { ContactCard } from './components/ContactCard';
import { ContactDetails } from './components/ContactDetails';
import { ContactForm } from './components/ContactForm';
import { Search, Plus, Users } from 'lucide-react';
import './styles/variables.css';
import './styles/App.css';

const App: React.FC = () => {
  const { contacts, addContact, updateContact, deleteContact } = useContacts();
  const [selectedId, setSelectedId] = useState<string | null>(null);
  const [searchQuery, setSearchQuery] = useState('');
  const [isFormOpen, setIsFormOpen] = useState(false);
  const [editingContact, setEditingContact] = useState<Contact | undefined>(undefined);

  // Filter contacts based on search query
  const filteredContacts = useMemo(() => {
    return contacts
      .filter((c) =>
        c.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
        c.phone.includes(searchQuery)
      )
      .sort((a, b) => a.name.localeCompare(b.name));
  }, [contacts, searchQuery]);

  const selectedContact = contacts.find((c) => c.id === selectedId);

  const handleAdd = () => {
    setEditingContact(undefined);
    setIsFormOpen(true);
  };

  const handleEdit = (contact: Contact) => {
    setEditingContact(contact);
    setIsFormOpen(true);
  };

  const handleSubmitForm = (data: Omit<Contact, 'id' | 'createdAt'>) => {
    if (editingContact) {
      updateContact(editingContact.id, data);
    } else {
      const newContact = addContact(data);
      setSelectedId(newContact.id);
    }
    setIsFormOpen(false);
  };

  const handleDelete = (id: string) => {
    if (window.confirm('Are you sure you want to delete this contact?')) {
      deleteContact(id);
      setSelectedId(null);
    }
  };

  return (
    <div className="app-container">
      {/* Sidebar */}
      <aside className="sidebar">
        <div className="sidebar-header">
          <h1 className="sidebar-title">
            <Users size={28} />
            Contacts
          </h1>
          <div className="search-bar-container">
            <Search className="search-icon" size={18} />
            <input
              type="text"
              placeholder="Search contacts..."
              className="search-input"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
            />
          </div>
          <button className="add-btn-sidebar" onClick={handleAdd}>
            <Plus size={20} />
            Add Contact
          </button>
        </div>

        <div className="contacts-list">
          {filteredContacts.map((contact) => (
            <ContactCard
              key={contact.id}
              contact={contact}
              active={selectedId === contact.id}
              onClick={() => setSelectedId(contact.id)}
            />
          ))}
          {filteredContacts.length === 0 && (
            <p className="no-results">No contacts found</p>
          )}
        </div>
      </aside>

      {/* Main Content Area */}
      <main className="main-content">
        {selectedContact ? (
          <ContactDetails
            contact={selectedContact}
            onEdit={() => handleEdit(selectedContact)}
            onDelete={() => handleDelete(selectedContact.id)}
          />
        ) : (
          <div className="empty-state">
            <Users size={64} className="empty-icon" />
            <h3>Your Address Book</h3>
            <p>Select a contact to view details or create a new one.</p>
          </div>
        )}
      </main>

      {/* Form Modal */}
      {isFormOpen && (
        <ContactForm
          contact={editingContact}
          onSubmit={handleSubmitForm}
          onCancel={() => setIsFormOpen(false)}
        />
      )}
    </div>
  );
};

export default App;
