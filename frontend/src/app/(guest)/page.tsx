import { redirect } from "next/navigation";

import { Camera, Cloud, MapPin } from "lucide-react";

import { getCurrentUser } from "@/lib/auth/utils";

import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";

const features = [
  {
    id: 1,
    icon: Camera,
    title: "Upload Photos",
    description:
      "Upload photos from your mountain adventures. Our system automatically reads location and time data.",
  },
  {
    id: 2,
    icon: MapPin,
    title: "Auto Peak Detection",
    description:
      "Our system automatically matches your location to Polish mountain peaks and suggests the correct summit.",
  },
  {
    id: 3,
    icon: Cloud,
    title: "Weather History",
    description:
      "See the weather conditions from the day of your climb, making your memories more complete and informative.",
  },
];

export default async function Home() {
  const user = await getCurrentUser();
  if (user) redirect(`/diary/${user.username}`);

  return (
    <>
      {/* Hero Section */}
      <section className="text-primary-foreground from-primary relative bg-gradient-to-b to-[var(--hero-gradient-to)]">
        <div className="absolute inset-0 overflow-hidden opacity-50">
          <div
            className="absolute inset-0 bg-[url('/mountains-pattern.svg')] bg-bottom bg-no-repeat"
            style={{ backgroundSize: "cover" }}
          ></div>
        </div>
        <div className="relative z-10 mx-auto max-w-7xl px-4 py-24 sm:px-6 md:py-32 lg:px-8">
          <div className="max-w-3xl">
            <h1 className="mb-6 text-4xl font-bold tracking-tight sm:text-5xl">
              Document Your Mountain Adventures
            </h1>
            <p className="text-primary-foreground/90 mb-8 text-xl">
              Track and share your conquests of Polish peaks with weather data,
              locations, and beautiful memories.
            </p>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="bg-muted/30 py-16">
        <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
          <div className="mb-16 text-center">
            <h2 className="text-foreground mb-4 text-3xl font-bold">
              How It Works
            </h2>
            <p className="text-muted-foreground mx-auto max-w-2xl text-xl">
              Easily upload and organize your mountain adventures with smart
              features.
            </p>
          </div>

          <div className="grid gap-8 md:grid-cols-3">
            {features.map((feature) => (
              <Card key={feature.id}>
                <CardHeader>
                  <div className="bg-primary/15 text-primary mb-4 flex h-12 w-12 items-center justify-center rounded-full">
                    <feature.icon className="h-6 w-6" />
                  </div>
                  <CardTitle>{feature.title}</CardTitle>
                </CardHeader>
                <CardContent>
                  <CardDescription className="text-base">
                    {feature.description}
                  </CardDescription>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="bg-primary text-primary-foreground py-16">
        <div className="mx-auto max-w-7xl px-4 text-center sm:px-6 lg:px-8">
          <h2 className="mb-6 text-3xl font-bold">
            Ready to document your mountain adventures?
          </h2>
          <p className="text-primary-foreground/90 mx-auto mb-8 max-w-3xl text-xl">
            Join our community of mountain enthusiasts and start tracking your
            conquests of Polish peaks.
          </p>
        </div>
      </section>
    </>
  );
}
