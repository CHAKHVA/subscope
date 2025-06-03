'use client'; 

import { useState } from 'react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';

export default function RegisterPage() {
  const [fullName, setFullName] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');

  const handleSubmit = (event: React.FormEvent) => {
    event.preventDefault();
    console.log({ fullName, email, password, confirmPassword });
  
    if (password !== confirmPassword) {
      alert("Passwords do not match!");
      return;
    }
    console.log(fullName, email, password, confirmPassword)
    alert('Registration Completed');
  };
  
  function handleNameChange(event: React.ChangeEvent<HTMLInputElement>){
    setFullName(event.target.value)
  }

  function handleEmailChange(event: React.ChangeEvent<HTMLInputElement>){
    setEmail(event.target.value)
  }

  function handlePasswordChange(event: React.ChangeEvent<HTMLInputElement>){
    setPassword(event.target.value)
  }

  function handlePasswordConfirmChange(event: React.ChangeEvent<HTMLInputElement>){
    setConfirmPassword(event.target.value)
  }


  return (
    <div className="flex justify-center items-center min-h-screen">
      <form onSubmit={handleSubmit} className="space-y-4 p-8 border rounded-lg shadow-md w-full max-w-md">
        <h2 className="text-2xl font-bold text-center">Create an Account</h2>
        <div>
          <Label htmlFor="fullName">Full Name</Label>
          <Input id="fullName" value={fullName} onChange={handleNameChange} />
        </div>
        <div>
          <Label htmlFor="email">Email</Label>
          <Input id="email" type="email" value={email} onChange={handleEmailChange} required />
        </div>
        <div>
          <Label htmlFor="password">Password</Label>
          <Input id="password" type="password" value={password} onChange={handlePasswordChange} required />
        </div>
        <div>
          <Label htmlFor="confirmPassword">Confirm Password</Label>
          <Input id="confirmPassword" type="password" value={confirmPassword} onChange={handlePasswordConfirmChange} required />
        </div>
        <Button type="submit" className="w-full">Register</Button>
      </form>
    </div>
  );
}